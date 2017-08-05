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
    """The Bug class represents a Bugzilla bug report."""
    def __init__(self,
                 bug_number,
                 summary=None,
                 comment=None,
                 resolution=None,
                 status=None):
        """Instanciates a bug report."""
        self.bug_number = bug_number
        self.summary = summary
        self.resolution = resolution
        self.status = status
        self.comment = comment

    def __str__(self):
        """String representation of a bug report."""
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
