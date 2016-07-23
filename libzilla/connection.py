################################################################################
#
# Copyright (c) 2016 Patrice Clement
#
# This file is part of libzilla
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

import requests
import logging
import json
import sys
import re

from libzilla.configmanager import ConfigManager
from libzilla.resturlmaker import RESTURLMaker

from libzilla.bug import Bug

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

"""The Connection class is in charge of talking to the Bugzilla REST API."""


class Connection:
    def __init__(self, debug=None):
        self.connected = False
        self.debug = debug
        self.configmanager = ConfigManager()
        self.rcfile = self.configmanager.obtain_credentials()
        self.resturlmaker = RESTURLMaker(url=self.rcfile['url'])

    def __str__(self):
        return '<{0} <id={1}> <url=\'{2}\'> <connected={3}> <token={4}>>'.format(
            self.__class__.__name__,
            id(self),
            self.rcfile['url'],
            self.connected,
            self.token
        )

    def login(self):
        if self.connected: return self.connected

        url = self.resturlmaker.make_login_url(
            username=self.rcfile['username'],
            password=self.rcfile['password']
        )

        logger.info('Logging in ...')
        response = self.send_request('GET', url)

        try:
            self.token = response.json()['token']
        except KeyError:
            logger.error('Login failed! Please check your credentials!')
            sys.exit(1)

        self.token = response.json()['token']
        self.resturlmaker.token = self.token
        self.connected = True
        logger.info('Logged in!')

        self.configmanager.save_rcfile()

        return self.connected

    def send_request(self, request_type='', url=None, data=None):
        if data: data = json.dumps(data)

        http_request = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'data': data,
            'url': url
        }

        if request_type == 'GET':
            response = requests.get(**http_request)
        elif request_type == 'PUT':
            response = requests.put(**http_request)
        elif request_type == 'POST':
            response = requests.post(**http_request)
        else:
            logger.error('You must specify a request type!')
            sys.exit(1)

        if response.status_code != 200:
            logger.error('HTTP code returned: {0} -> {1}'
                         .format(response.status_code,
                                 response.reason))

        return response

    def get_bug_info(self, bug_number):
        url = self.resturlmaker.make_bug_url(
            bug_number=bug_number
        )

        logger.info('Querying Bugzilla for bug #{0} ...'.format(bug_number))
        response = self.send_request('GET', url)

        try:
            response = response.json()['bugs'][0]
        except KeyError:
            logger.error('Bug #{0} does not exist in the Bugzilla DB!'
                         .format(bug_number))
            sys.exit(1)

        if re.search(r'[a-zA-Z]+', bug_number):
            fmt = 'More info about this bug: \
https://bugs.gentoo.org/show_bug.cgi?id={0}' \
                  .format(bug_number)
        else:
            fmt = 'More info about this bug: \
https://bugs.gentoo.org/{0}' \
                  .format(bug_number)

        logger.info(fmt)

        bug = Bug(
            bug_number=bug_number,
            summary=response['summary'],
            resolution=response['resolution'],
            status=response['status']
        )

        if bug.resolution == '': bug.resolution = 'NONE'

        for key, value in bug.__dict__.items():
            key = str(key)
            if key == 'bug_number': key = 'Bug #'
            if key in ('resolution', 'status'): key = key.upper()
            else: key = key.capitalize()
            logger.info('{0}: {1}'.format(key, value))

        return bug

    def update_bugs(self, list_of_bugs):
        for bug in list_of_bugs:
            bug_number = bug.bug_number
            resolution = bug.resolution
            comment = bug.comment
            status = bug.status

            url = self.resturlmaker.make_bug_url(
                bug_number=bug.bug_number
            )

            if not status and not resolution and not comment:
                logger.info('Nothing to update for bug #{0}.'
                            .format(bug_number))
                break

            data = {
                'ids': bug_number,
                'token': self.token,
                'comment': {'body': comment}
            }

            if status and status != '':
                data['status'] = status
                logger.info('Setting STATUS to {0} ...'
                            .format(status))

            if resolution and resolution != '':
                data['resolution'] = resolution
                logger.info('Setting RESOLUTION to {0} ...'
                            .format(resolution))

            if comment and comment != '':
                logger.info('Posting comment to bug #{0} ...'
                            .format(bug_number))

            response = self.send_request('PUT', url, data)

            if not response.ok: sys.exit(1)

            logger.info('OK!')

    def file_bug(self, data):
        url = self.resturlmaker.make_new_bug_url()
        data['token'] = self.token
        logger.info('Filing bug ...')
        response = self.send_request('POST', url, data)

        if not response.ok: sys.exit(1)

        logger.info('OK!')

        bug_id = response.json()['id']
        logger.info('New bug filed at https://bugs.gentoo.org/{0}'
                    .format(bug_id))

        return response
