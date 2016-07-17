"""This modules defines the BugCommand class.

The BugCommand class is the entry point into the `lzilla bug' command which
helps manage bug from the CLI on the fly."""

from libzilla.connection import Connection
from libzilla.bug import Bug


class BugCommand:
    """lzilla bug: Query or alter one or more bug number(s).

Usage:
  lzilla bug <bug_number> ...
  lzilla bug <bug_number> ... [-r=<r>] [-s=<s>] [-c=<c>] [-h]

Options:
  -h, --help                     Display help.
  -r, --resolution=<resolution>  Set RESOLUTION to bug report(s).
  -s, --status=<status>          Set STATUS to bug report(s).
  -c, --comment=<comment>        Comment to add to bug report(s).

Examples:
  lzilla bug 12345 --comment 'Fix pushed, thanks!'
  lzilla bug 12345 --resolution FIXED --status RESOLVED"""

    def __init__(self, args):
        args['<bug_number>'] = set(args['<bug_number>'])

        attrs = {
            'resolution': args['--resolution'],
            'comment': args['--comment'],
            'status': args['--status']
        }

        conn = Connection()
        conn.login()
        bugs = args['<bug_number>']
        list_of_bugs = []

        for bug_number in bugs:
            bug = conn.get_bug_info(bug_number)
            list_of_bugs.append(Bug(bug_number=bug.bug_number))

        for attr, value in attrs.items():
            Bug.set_bug_attr(attr, value, list_of_bugs)

        conn.update_bugs(list_of_bugs)
