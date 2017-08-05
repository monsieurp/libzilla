##############################################################################
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
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
##############################################################################

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


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)


class ConfigManager(ConfigParser):
    """The ConfigManager is a wrapper around the ~/.libzillarc file.
    This class contains functions to read the aforementioned file, work
    out the user's credentials and more."""
    def __init__(self):
        """Instanciate a ConfigManager object."""
        super().__init__(default_section=DEFAULT_SECTION)
        self.read([DEFAULT_RCFILE])
        self.rcfile = {}

    def __str__(self):
        """Return a string representation of a ConfigManager instance."""
        return '<{0} <id={1}> <rcfile={2}>>'.format(
            self.__class__.__name__,
            id(self),
            self.rcfile
        )

    def obtain_credentials(self):
        """Get the user's credentials from the rcfile."""
        if not os.path.exists(DEFAULT_RCFILE):
            logger.info('File \"{0}\" not found! Prompt user for credentials.'
                        .format(DEFAULT_RCFILE))
            credentials = collections.OrderedDict()
            self.rcfile = prompt_for_credentials(credentials)
        else:
            logger.info('File \"{0}\" found!'.format(DEFAULT_RCFILE))
            self.walk_rcfile()

        return self.rcfile

    def save_rcfile(self):
        """Write out the rcfile content to disk."""
        if os.path.exists(DEFAULT_RCFILE):
            return

        if prompt('Would you like to record these settings in {0}? [y/n] '
                  .format(DEFAULT_RCFILE)) != 'y':
            info_msg = 'Keeping settings in memory'
            info_msg += ' for the remaining of the session'
            logger.info(info_msg)
            return

        logger.info('Storing settings in \"{0}\" ...'.format(DEFAULT_RCFILE))
        for item in self.rcfile:
            self.set(DEFAULT_SECTION, item, self.rcfile[item])

        with open(DEFAULT_RCFILE, 'w') as rcfile:
            self.write(rcfile)

        os.chmod(DEFAULT_RCFILE, 0o600)
        logger.info('Settings successfully recorded!')

    def walk_rcfile(self):
        """Walk the rcfile content and retrieve information."""
        for item in self.items(DEFAULT_SECTION):
            k, v = item
            self.rcfile[k] = v

        try:
            for key in KEYS_IN_RCFILE:
                self.rcfile[key]
        except KeyError as e:
            import sys
            logger.error('Missing key in .libzillarc: \"{0}\" not found'.
                         format(e))
            sys.exit(1)

        self.rcfile['url'] = validator.validate_url(self.rcfile['url'])
