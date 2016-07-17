import sys

ERROR_MESSAGES = {
    'options': 'Both options -s/--status -r/--resolution must be specified!',
    'bug_number': 'Error! Bug \"{0}\" in an invalid bug number!',
    'resolution': 'Error! RESOLUTION \"{0}\" not found in:\n{1}',
    'status': 'Error! STATUS \"{0}\" not found in:\n{1}'
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
    'TEST-REQUEST'
]

STATUSES = [
    'RESOLVED',
    'VERIFIED',
    'CONFIRMED',
    'UNCONFIRMED'
]


class Bug:
    def __init__(self,
                 bug_number,
                 summary=None,
                 comment=None,
                 resolution=None,
                 status=None):

        self.bug_number = bug_number
        self.summary = summary
        self.resolution = resolution
        self.status = status
        self.comment = comment

    def __str__(self):
        return """Bug #: %s
Summary: %s
RESOLUTION: %s
STATUS: %s
Comment: %s""" % (
            self.bug_number,
            self.summary,
            self.resolution,
            self.status,
            self.comment
        )

    @staticmethod
    def set_bug_attr(attr, value, bugs):
        if not attr or attr == '':
            return

        if value and \
           attr == 'resolution' and \
           value not in RESOLUTIONS:
            print(ERROR_MESSAGES['resolution']
                  .format(value, RESOLUTIONS))
            sys.exit(1)

        if value and \
           attr == 'status' and \
           value not in STATUSES:
            print(ERROR_MESSAGES['status']
                  .format(value, STATUSES))
            sys.exit(1)

        if value and \
           value != '':
            for bug in bugs:
                bug.__setattr__(attr, value)
