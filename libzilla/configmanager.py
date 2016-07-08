from libzilla.exceptions import LibZillaException
from libzilla.promptmaker import prompt_for_credentials
from libzilla.promptmaker import prompt
from configparser import ConfigParser

import libzilla.validator as validator
import collections
import logging
import os

DEFAULT_RCFILE = os.path.expanduser('~/.libzillarc')
DEFAULT_TOKENFILE = os.path.expanduser('~/.libzillatoken')
DEFAULT_SECTION = 'gentoo'
KEYS_IN_RCFILE = 'url username password'.split()

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)


class ConfigManager(ConfigParser):
    def __init__(self):
        super().__init__(default_section=DEFAULT_SECTION)
        self.read([DEFAULT_RCFILE])
        self.rcfile = {}

    def __str__(self):
        return '<{0} <id={1}> <rcfile={2}>>'.format(
            self.__class__.__name__,
            id(self),
            self.rcfile
        )

    def obtain_credentials(self):
        if not os.path.exists(DEFAULT_RCFILE):
            logger.info('File \"{0}\" not found! Prompt user for credentials.'.format(DEFAULT_RCFILE))
            credentials = collections.OrderedDict()
            self.rcfile = prompt_for_credentials(credentials)
            if prompt('Would you like to record these settings in {0}? [y/n] '.format(DEFAULT_RCFILE)) == 'y':
                self.save_rcfile()
            else:
                logger.info('Keeping settings in memory for the remaining of the session.')
        else:
            logger.info('File \"{0}\" found!'.format(DEFAULT_RCFILE))
            self.walk_rcfile()

        return self.rcfile

    def save_rcfile(self):
        logger.info('Storing settings in \"{0}\" ...'.format(DEFAULT_RCFILE))
        for item in self.rcfile:
            self.set(DEFAULT_SECTION, item, self.rcfile[item])

        with open(DEFAULT_RCFILE, 'w') as rcfile:
            self.write(rcfile)

        os.chmod(DEFAULT_RCFILE, 0o600)
        logger.info('Settings successfully recorded!')

    def walk_rcfile(self):
        for item in self.items(DEFAULT_SECTION):
            k, v = item
            self.rcfile[k] = v

        try:
            for key in KEYS_IN_RCFILE:
                self.rcfile[key]
        except KeyError as e:
            raise LibZillaException('Missing key in .libzillarc: \"{0}\" not found'.format(e))

        self.rcfile['url'] = validator.validate_url(self.rcfile['url'])
