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

from libzilla.git.toolbox import look_for_bug_numbers
from libzilla.git.toolbox import trim_spaces
from libzilla.git.toolbox import run_command

GIT_COMMAND = 'git --no-pager log --pretty --summary --color=never --stat --format=fuller -1 HEAD'

CANDIDATES = (
    r'^.*?Fixes bug (\d+).*?$',
    r'^.*?Fixes security bug (\d+).*?$',
    r'^\s+Gentoo-Bug:(\s+\d+)$',
    r'^\s+Gentoo-Bug:\s?https://bugs.gentoo.org/(\d+)'
)

"""A GitSession represents a `git' command run."""


class GitSession:
    def __init__(self):
        self.commit_info = None
        self.begin()

    def begin(self):
        last_commit = run_command(GIT_COMMAND)

        bugs_to_close = set(
            filter(lambda bug: bug, \
            map(lambda line: look_for_bug_numbers(line, CANDIDATES), last_commit))
        )

        self.commit_info = {
            'bugs_to_close': bugs_to_close,
            'content': trim_spaces(last_commit),
            'len_bugs': len(bugs_to_close)
        }
