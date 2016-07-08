from libzilla.session import LibzillaSession

""" This modules defines the BugCommand class. """


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
        session = LibzillaSession(args)
        session.check_for_args()
        session.connect()
        session.process_bug_numbers()
        session.update_bugs()
