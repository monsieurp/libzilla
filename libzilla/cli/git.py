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
