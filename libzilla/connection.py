import collections
import requests
import logging
import json

from libzilla.exceptions import LibZillaException
from libzilla.resturlmaker import RESTURLMaker
from libzilla.configmanager import ConfigManager

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, debug=None):
        self.connected = False
        self.debug = debug
        self.rcfile = ConfigManager().obtain_credentials()
        self.resturlmaker = RESTURLMaker(url=self.rcfile['url'])

    def __str__(self):
        return '<{0} <id={1}> <url=\'{2}\'> <connected={3}> <token={4}>>'.format(
            self.__class__.__name__,
            id(self),
            self.rcfile['url'],
            self.connected,
            self.token
        )

    def send_request(self, request_type='', url=None, payload=None):
        if payload:
            payload = json.dumps(payload)

        http_request = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'data': payload,
            'url': url
        }

        if request_type == 'GET':
            response = requests.get(**http_request)
        elif request_type == 'PUT':
            response = requests.put(**http_request)
        else:
            raise LibZillaException('You must specify a request type!')

        if response.status_code != 200:
            raise LibZillaException(response.reason)

        return response

    def login(self):
        if self.connected:
            return self.connected

        url = self.resturlmaker.make_login_url(
            username=self.rcfile['username'],
            password=self.rcfile['password']
        )
        logger.info('Logging in ...')
        response = self.send_request('GET', url)
        self.token = response.json()['token']
        self.resturlmaker.token = self.token
        self.connected = True
        logger.info('Logged in!')
        return self.connected

    def get_bug_info(self, bug_number):
        url = self.resturlmaker.make_bug_url(
            bug_number=bug_number
        )

        logger.info('Querying Bugzilla for bug #{0} ...'.format(bug_number))

        response = self.send_request('GET', url)
        if len(response.json()['bugs']) == 0:
            raise LibZillaException('Bug \"{0}\" does not exist in the Bugzilla DB!'.format(bug_number))
        response = response.json()['bugs'][0]

        logger.info('More info about this bug: https://bugs.gentoo.org/{0}.'
                    .format(bug_number))

        info = collections.OrderedDict({
            'resolution': response['resolution'],
            'summary': response['summary'],
            'status': response['status']
        })

        if info['resolution'] == '':
            info['resolution'] = 'NONE'

        for key, value in info.items():
            key = str(key)
            if key == 'summary':
                key = key.capitalize()
            else:
                key = key.upper()
            logger.info('{0}: {1}'.format(key, value))

        return info

    def update_bugs(self, updates):
        for bug_number, update in updates.items():
            url = self.resturlmaker.make_bug_url(
                bug_number=bug_number,
                token=False
            )

            resolution = update.get('resolution')
            comment = update.get('comment')
            status = update.get('status')

            if not status and not resolution and not comment:
                logger.info('Nothing to update for bug {0}.'.format(bug_number))
                break

            payload = {
                'ids': bug_number,
                'token': self.token,
                'comment': {
                    'body': comment
                }
            }

            if status and status != '':
                payload['status'] = status
                logger.info('Setting STATUS to {0} ...'.format(status))

            if resolution and resolution != '':
                payload['resolution'] = resolution
                logger.info('Setting RESOLUTION to {0} ...'.format(resolution))

            if comment != '':
                logger.info('Posting comment to bug {0} ...'.format(bug_number))

            response = self.send_request('PUT', url, payload)
            if not response.ok:
                raise LibZillaException('An error occured whilst updating {0}: \"{1}\"'.format(
                    bug_number,
                    response.ok
                    )
                )

            logger.info('OK!')

        return True
