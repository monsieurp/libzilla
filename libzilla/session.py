from libzilla import Connection
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

""" This module defines the LibzillaSession class. """

ERROR_MESSAGES = {
    'bug_number': 'Error! Bug \"{0}\" in an invalid bug number!',
    'options': 'Both options -s/--status -r/--resolution must be specified!',
    'resolution': 'Error! RESOLUTION \"{0}\" not in\n{1}',
    'status': 'Error! STATUS \"{0}\" not in\n{1}'
}

RESOLUTIONS = [
    'FIXED',
    'INVALID',
    'WONTFIX',
    'CANTFIX',
    'NEEDINFO',
    'UPSTREAM',
    'OBSOLETE',
    'DUPLICATE',
    'WORKSFORME',
    'TEST-REQUEST',
]

STATUSES = [
    'UNCONFIRMED',
    'CONFIRMED',
    'RESOLVED',
    'VERIFIED'
]


class LibzillaSession:
    def __init__(self, args):
        self.args = args
        self.bugs = {}
        self.conn = None

    def connect(self):
        if not self.conn: self.conn = Connection()
        self.conn.login()

    def get_bug_info(self, bug_number):
        return self.conn.get_bug_info(bug_number)

    def update_bugs(self):
        return self.conn.update_bugs(self.bugs)

    def check_for_bug_numbers(self, args=None):
        if args:
            my_args = args
        else:
            my_args = self.args

        bug_numbers = my_args['<bug_number>']
        for bug in bug_numbers:
            try:
                bug = int(bug)
            except ValueError:
                print(ERROR_MESSAGES['bug_number']
                      .format(bug))
                return False
        return True

    def check_for_options(self, args=None):
        if args:
            my_args = args
        else:
            my_args = self.args

        resolution = my_args['--resolution']
        status = my_args['--status']
        if (resolution and not status) or \
           (not resolution and status):
            print(ERROR_MESSAGES['options'])
            return False
        return True

    def check_for_resolution(self, res=None):
        if res:
            resolution = res
        else:
            resolution = self.args['--resolution']

        if resolution and resolution not in RESOLUTIONS:
            print(ERROR_MESSAGES['resolution']
                  .format(resolution, RESOLUTIONS))
            return False
        return True

    def check_for_status(self, st=None):
        if st:
            status = st
        else:
            status = self.args['--status']
        if status and status not in STATUSES:
            print(ERROR_MESSAGES['status']
                  .format(status, STATUSES))
            return False
        return True

    def check_for_args(self):
        all_fcnts = (
            self.check_for_bug_numbers(),
            self.check_for_options(),
            self.check_for_resolution(),
            self.check_for_status()
        )

        if not all(all_fcnts):
            sys.exit(1)

    def process_bug_numbers(self, bugs=None):
        if bugs:
            my_args = bugs
        else:
            my_args = self.args

        bug_numbers = my_args['<bug_number>']
        for bug_number in bug_numbers:
            self.get_bug_info(bug_number)
            self.bugs[bug_number] = {
                'resolution': my_args['--resolution'],
                'comment': my_args['--comment'],
                'status': my_args['--status']
            }
