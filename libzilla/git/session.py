from libzilla.git.toolbox import look_for_bug_numbers
from libzilla.git.toolbox import trim_spaces
from libzilla.git.toolbox import run_command
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

GIT_COMMAND = 'git --no-pager log --decorate --pretty --summary --color=never --stat --format=fuller -1 HEAD'


class GitSession:
    def __init__(self):
        self.commit_info = {}
        self.begin()

    def begin(self):
        last_commit = run_command(GIT_COMMAND)

        bugs_to_close = set(
            filter(lambda bug: bug, \
            map(lambda line: look_for_bug_numbers(line), last_commit))
        )

        self.commit_info = {
            'bugs_to_close': bugs_to_close,
            'content': trim_spaces(last_commit),
            'len_bugs': len(bugs_to_close)
        }

    def get_len_bugs(self):
        return self.commit_info['len_bugs']
