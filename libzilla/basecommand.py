import sys
from docopt import docopt

"""The BaseCommand class is an entry point into the `lzilla' command which
dispatches keywords to sub commands."""

VERSION = '1.0'


class BaseCommand:
    """lzilla is a tool for managing Bugzilla bug reports.

All communications are carried out using
the Bugzilla REST API over the HTTPS scheme.

Usage:
  lzilla [-h|--help] <command> [<args>...]

Commands:
  lzilla stable
  lzilla shell
  lzilla bug
  lzilla git

Options:
  -h,  --help     Display help.
  -v,  --version  Display version."""

    def __init__(self):
        args = docopt(
            BaseCommand.__doc__,
            version=VERSION,
            help=True,
            options_first=True
        )

        runner = {
            'stable': self.run_stable_command,
            'shell':  self.run_shell_command,
            'bug':    self.run_bug_command,
            'git':    self.run_git_command
        }

        try:
            runner[args['<command>']]()
        except KeyError:
            sys.exit("Error! \'{0}\' is an invalid command.\nSee 'lzilla --help' for a complete list of commands."
                     .format(args['<command>']))

    def run_bug_command(self):
        from libzilla.cli.bug import BugCommand
        BugCommand(docopt(BugCommand.__doc__))

    def run_git_command(self):
        from libzilla.cli.git import GitCommand
        GitCommand(docopt(GitCommand.__doc__))

    def run_stable_command(self):
        from libzilla.cli.stable import StableCommand
        StableCommand(docopt(StableCommand.__doc__))

    def run_shell_command(self):
        from libzilla.cli.shell import ShellCommand
        ShellCommand(docopt(ShellCommand.__doc__)).cmdloop()
