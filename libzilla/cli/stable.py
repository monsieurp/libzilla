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

from libzilla.promptmaker import prompt
from portage.xml.metadata import MetaDataXML
from libzilla.connection import Connection
import portage
import sys
import os

"""This modules defines the StableCommand class.

The StableCommand class is the entry point into the `lzilla stable' command
which helps file stabilisation requests from the CLI."""

ERROR_MESSAGES = {
    'file_not_found': 'Error! File \"{0}\" does not exist!',
    'keywords': 'Error! No KEYWORDS found in \"{0}\"',
    'ebuild': 'Error! File \"{0}\" is not an ebuild!'
}

DESCRIPTION = """Arch teams,

Please stabilise:
{0}

Target arches:
{1}

Thank you!"""


class StableCommand:
    """lzilla stable: File a stabilisation request.

WARNING! This is a Gentoo-specific command.

Usage:
  lzilla stable <ebuild>

Options:
  -h, --help                     Display help.

Examples:
  lzilla stable GD-2.560.0-r1.ebuild
  lzilla stable /usr/portage/dev-perl/Moo/Moo-2.0.2.ebuild"""

    def __init__(self, args):
        self.metadata = None
        self.ebuild = None
        self.split = None

        self.maintainers = []
        self.arches = []
        self.cc = []

        self.initialise_files(args['<ebuild>'])
        self.look_for_maintainers()
        self.look_for_keywords()

        self.conn = Connection()
        self.conn.login()

        promptmsg = """Ebuild: {0}
Arches: {1}
File stabilisation request? [y/n] """.format(self.ebuild, ', '.join(self.arches))
        if prompt(promptmsg) == 'y':
            self.file_stabilisation_request()

    def initialise_files(self, ebuild):
        if not os.path.isfile(ebuild):
            sys.exit(ERROR_MESSAGES['file_not_found'].format(ebuild))

        if not ebuild.endswith('.ebuild'):
            sys.exit(ERROR_MESSAGES['ebuild'].format(ebuild))

        self.ebuild = os.path.realpath(ebuild)
        self.metadata = os.path.dirname(self.ebuild) + '/metadata.xml'

    def look_for_maintainers(self):
        pkg_md = MetaDataXML(self.metadata, herds=None)
        for maint in pkg_md.maintainers():
            self.maintainers.append(maint.email)

        if len(self.maintainers) == 0:
            self.maintainers.append('maintainer-needed@gentoo.org')

    def look_for_keywords(self):
        # work out ebuild's category
        split = self.ebuild.split(os.sep)
        split.pop()
        split.pop()
        cat = split.pop()

        # work out ebuild's name
        ebuild = os.path.basename(self.ebuild)
        ebuild = os.path.splitext(ebuild)[0]
        self.ebuild = '{0}/{1}'.format(cat, ebuild)

        # perform look up
        mysettings = portage.config(local_config=False)
        dbapi = portage.portdbapi(mysettings=mysettings)
        dbapi.porttrees = [dbapi.porttree_root]
        keywords = dbapi.aux_get(self.ebuild, ['KEYWORDS'], dbapi.porttree_root)[0]

        if len(keywords) == 0:
            sys.exit(ERROR_MESSAGES['keywords'].format(ebuild))

        for arch in keywords.split():
            # keep keywords in ~arch only
            if '~' in arch:
                # skip "exotic" arches such as ~amd64-macos and such
                if '-' in arch: continue
                arch = arch.strip('~')
                self.arches.append(arch)
                self.cc.append(arch + '@gentoo.org')

    def file_stabilisation_request(self):
        assignee = self.maintainers.pop()
        if len(self.maintainers) > 0:
            for maintainer in self.maintainers:
                self.cc.append(maintainer)

        summary = '={0}: stabilisation request'.format(self.ebuild)

        stablereq = {
            'status': 'CONFIRMED',
            'summary': summary,
            'assigned_to': assignee,
            'version': 'unspecified',
            'product': 'Gentoo Linux',
            'severity': 'normal',
            'component': 'Current packages',
            'description': DESCRIPTION.format(
                '=' + self.ebuild,
                ', '.join(self.arches)
            ),
            'priority': 'normal',
            'cc': self.cc,
            'keywords': ['STABLEREQ']
        }

        self.conn.file_bug(stablereq)
