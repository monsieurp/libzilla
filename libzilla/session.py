from libzilla.connection import Connection
import sys

"""This module defines the Session class."""

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


class Session:
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

    def check_for_options(self, args=None):
        my_args = self.args
        if args:
            my_args = args

        resolution = my_args['--resolution']
        status = my_args['--status']
        retval = True
        if (resolution and not status) or \
           (not resolution and status):
            print(ERROR_MESSAGES['options'])
            retval = False
        return retval

    def check_for_resolution(self, res=None):
        resolution = self.args['--resolution']
        if res:
            resolution = res

        retval = True
        if resolution and resolution not in RESOLUTIONS:
            print(ERROR_MESSAGES['resolution']
                  .format(resolution, RESOLUTIONS))
            retval = False
        return retval

    def check_for_status(self, st=None):
        status = self.args['--status']
        if st:
            status = st

        retval = True
        if status and status not in STATUSES:
            print(ERROR_MESSAGES['status']
                  .format(status, STATUSES))
            retval False
        return retval

    def check_for_args(self):
        all_functs = (
            self.check_for_resolution(),
            self.check_for_options(),
            self.check_for_status()
        )

        if not all(all_functs):
            sys.exit(1)

    def process_bug_numbers(self, bugs=None):
        my_args = self.args
        if bugs:
            my_args = bugs

        bug_numbers = my_args['<bug_number>']
        for bug_number in bug_numbers:
            self.get_bug_info(bug_number)
            self.bugs[bug_number] = {
                'resolution': my_args['--resolution'],
                'comment': my_args['--comment'],
                'status': my_args['--status']
            }
