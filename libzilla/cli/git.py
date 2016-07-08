from libzilla.git.session import GitSession
from libzilla.session import LibzillaSession

"""This modules defines the GitCommand class."""


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

        args['<bug_number>'] = gitsession.commit_info['bugs_to_close']
        args['--comment'] = comment

        session = LibzillaSession(args)
        session.check_for_args()
        session.connect()
        session.process_bug_numbers()
        session.update_bugs()
