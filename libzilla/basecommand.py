import sys
from docopt import docopt

"""The BaseCommand class is an entry point into the `lzilla' command which
dispatches keywords to sub commands."""


class BaseCommand:
    """lzilla is a tool for managing Bugzilla bug reports.

All communications are carried out using
Bugzilla REST API over the HTTPS scheme.

Usage:
  lzilla [-h|--help] <command> [<args>...]

Commands:
  lzilla shell
  lzilla bug
  lzilla git

Options:
  -h,  --help     Display help.
  -v,  --version  Display version."""

    def __init__(self):
        args = docopt(
            BaseCommand.__doc__,
            version='0.1',
            help=True,
            options_first=True
        )

        if args['<command>'] == 'bug':
            from libzilla.cli.bug import BugCommand
            BugCommand(docopt(BugCommand.__doc__))
        elif args['<command>'] == 'git':
            from libzilla.cli.git import GitCommand
            GitCommand(docopt(GitCommand.__doc__))
        elif args['<command>'] == 'shell':
            from libzilla.cli.shell import ShellCommand
            ShellCommand(docopt(ShellCommand.__doc__)).cmdloop()
        else:
            sys.exit("Error! \'{0}\' is an invalid command.\nSee 'lzilla --help' for a complete list of commands."
                     .format(args['<command>']))
