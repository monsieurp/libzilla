"""This modules defines the GitCommand class."""

from libzilla.git.session import GitSession
from libzilla.connection import Connection
from libzilla.bug import Bug


class GitCommand:
    """lzilla git: Parse last git commit.

By default, the last commit is parsed
and used as comment.

Usage:
  lzilla git [-r=<r>] [-s=<s>] [-c=<c>]

Options:
  -h, --help                     Display help.
  -r, --resolution=<resolution>  Set RESOLUTION to parsed bug report(s).
  -s, --status=<status>          Set STATUS to parsed bug report(s).
  -c, --comment=<comment>        Append comment to parsed bug report(s).

Examples:
  lzilla git --comment 'Fix pushed, thanks!'
  lzilla git --resolution FIXED --status RESOLVED"""

    def __init__(self, args):
        gitsession = GitSession()
        gitsession.begin()
        comment = args['--comment']

        if comment:
            comment = '{0}\n\n{1}'.format(
                gitsession.commit_info['content'],
                comment
            )
        else:
            comment = gitsession.commit_info['content']

        if gitsession.commit_info['len_bugs'] == 0:
            import sys
            sys.exit('Error! No bug found in last commit!')

        attrs = {
            'resolution': args['--resolution'],
            'status': args['--status'],
            'comment': comment
        }

        bugs = gitsession.commit_info['bugs_to_close']
        conn = Connection()
        conn.login()
        list_of_bugs = []

        for bug_number in bugs:
            bug = conn.get_bug_info(bug_number)
            list_of_bugs.append(Bug(
                bug_number=bug.bug_number,
                comment=comment,
                resolution=args['--resolution'],
                status=args['--status']
            ))

        for attr, value in attrs.items():
            Bug.set_bug_attr(attr, value, list_of_bugs)

        conn.update_bugs(list_of_bugs)
