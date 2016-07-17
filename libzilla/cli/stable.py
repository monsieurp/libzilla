from portage.xml.metadata import MetaDataXML
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


class StableCommand:
    """lzilla stable: File a stabilisation request.

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

        self.initialise_files(args['<ebuild>'])
        self.look_for_maintainers()
        self.look_for_keywords()
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
        ebuild = '{0}/{1}'.format(cat, ebuild)

        # perform look up
        mysettings = portage.config(local_config=False)
        dbapi = portage.portdbapi(mysettings=mysettings)
        dbapi.porttrees = [dbapi.porttree_root]
        keywords = dbapi.aux_get(ebuild, ['KEYWORDS'], dbapi.porttree_root)[0]

        if len(keywords) == 0:
            sys.exit(ERROR_MESSAGES['keywords'].format(ebuild))

        for arch in keywords.split():
            # only keep keywords in ~arch
            if '~' in arch:
                # skip "exotic" arches such as ~amd64-macos and such
                if '-' in arch: continue
                self.arches.append(
                    arch.strip('~') + '@gentoo.org'
                )

    def file_stabilisation_request(self):
        print('Maintainers: ' + str(self.maintainers))
        print('Arches: ' + str(self.arches))
