from libzilla.git.toolbox import look_for_bug_numbers
from libzilla.git.toolbox import trim_spaces
from libzilla.git.toolbox import run_command

GIT_COMMAND = 'git --no-pager log --decorate --pretty --summary --color=never --stat --format=fuller -1 HEAD'

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
