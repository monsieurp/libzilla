##############################################################################
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
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
##############################################################################

import sys
from docopt import docopt


"""The BaseCommand class is an entry point into the `lzilla' command which
dispatches keywords to subcommands."""


VERSION = '1.5'


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
            sys.exit("""Error! \'%s\' is an invalid command!
See 'lzilla --help' for a complete list of commands.""" % (args['<command>']))

    def run_bug_command(self):
        """Run the `lzilla bug' command."""
        from libzilla.cli.bug import BugCommand
        BugCommand(docopt(BugCommand.__doc__))

    def run_git_command(self):
        """Run the `lzilla git' command."""
        from libzilla.cli.git import GitCommand
        GitCommand(docopt(GitCommand.__doc__))

    def run_stable_command(self):
        """Run the `lzilla stable' command."""
        from libzilla.cli.stable import StableCommand
        StableCommand(docopt(StableCommand.__doc__))

    def run_shell_command(self):
        """Run the `lzilla shell' command."""
        from libzilla.cli.shell import ShellCommand
        ShellCommand(docopt(ShellCommand.__doc__)).cmdloop()
