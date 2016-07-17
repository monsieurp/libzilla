from libzilla.connection import Connection

from libzilla.bug import RESOLUTIONS
from libzilla.bug import STATUSES

from libzilla.bug import Bug
import cmd

"""This module defines the ShellCommand class."""

INTRO = """Welcome to the Libzilla Shell!

For a complete list of commands, type help.
The current bug report # is {0}.

List of bug reports for this session: {1}"""


class ShellCommand(cmd.Cmd):
    """lzilla shell: Spawn an interactive shell using the cmd module.

Usage:
  lzilla shell <bug_number> ...

Options:
  -h, --help    Display help.

Examples:
  lzilla shell 1234
  lzilla shell 1234 2345"""

    def __init__(self, args):
        cmd.Cmd.__init__(self)

        args['<bug_number>'] = set(args['<bug_number>'])

        self.conn = Connection()
        self.conn.login()
        bugs = args['<bug_number>']
        list_of_bugs = []

        for bug_number in bugs:
            bug = self.conn.get_bug_info(bug_number)
            list_of_bugs.append(Bug(
                bug_number=bug.bug_number,
                resolution=bug.resolution,
                comment=bug.comment,
                summary=bug.summary,
                status=bug.status
            ))

        first_br = self.walk_list_of_bugs(list_of_bugs)

        self.prompt = '> '
        self.intro = INTRO.format(first_br.bug_number, ', '.join(bugs))

    def walk_list_of_bugs(self, list_of_bugs):
        first_br = list_of_bugs.pop()
        first = last = BugReport(first_br)
        for bug in list_of_bugs:
            last = last.add(bug)
        last.nexx = first
        first.previous = last
        self.current_br = first
        return first_br

    def do_comment(self, line):
        """Add comment to current bug report."""
        if not line:
            print('Sorry, comment cannot be empty!')
            return
        comment = self.current_br.bug.comment
        if comment:
            print('Comment was: {0}'.format(comment))
        else:
            print('There was no comment set.')
        self.current_br.bug.comment = line
        print('Comment is now: {0}'.format(line))

    def complete_status(self, text, line, start_index, end_index):
        """Complete status command."""
        if text:
            return [status for status in STATUSES if status.startswith(text)]
        else:
            return STATUSES

    def do_status(self, line):
        """Set STATUS to current bug report."""
        if not line:
            print('Sorry, STATUS cannot be empty!')
            return
        Bug.set_bug_attr('status', line, [self.current_br.bug])
        status = self.current_br.bug.status
        if status:
            print('STATUS was: {0}'.format(status))
        else:
            print('There was no STATUS set.')
        self.current_br.bug.status = line
        print('STATUS is now: {0}'.format(line))

    def complete_resolution(self, text, line, start_index, end_index):
        """Complete resolution command."""
        if text:
            return [resolution for resolution in RESOLUTIONS if resolution.startswith(text)]
        else:
            return RESOLUTIONS

    def do_resolution(self, line):
        """Set RESOLUTION to current bug report."""
        if not line:
            print('Sorry, RESOLUTION cannot be empty!')
            return
        Bug.set_bug_attr('resolution', line, [self.current_br.bug])
        resolution = self.current_br.bug.resolution
        if resolution:
            print('RESOLUTION was: {0}'.format(resolution))
        else:
            print('There was no RESOLUTION set.')
        self.current_br.bug.resolution = line
        print('RESOLUTION is now: {0}'.format(line))

    def do_info(self, line):
        """Print current bug report information."""
        print(self.current_br.bug)

    def do_query(self, line):
        """Query Bugzilla about current bug report i.e. status, \
resolution and summary."""
        self.conn.get_bug_info(self.current_br.bug_number)

    def do_update(self, line):
        """Update current bug report."""
        self.conn.update_bugs([self.current_br.bug])

    def do_next(self, line):
        """Switch to next bug report in the stack."""
        self.current_br = self.current_br.nexx
        print('Switch to next bug report: {0}'
              .format(self.current_br.bug.bug_number))

    def do_previous(self, line):
        """Switch to previous bug report in the stack."""
        self.current_br = self.current_br.previous
        print('Switch to previous bug report: {0}'
              .format(self.current_br.bug.bug_number))

    def do_EOF(self, line):
        """Quit shell by pressing ^D."""
        print('Bye!')
        return -1

    def do_quit(self, line):
        """Quit shell."""
        return self.do_EOF(line)


class BugReport:
    def __init__(self, bug, nexx=None, previous=None):
        self.bug = bug
        self.nexx = nexx
        self.previous = previous

    def add(self, bug):
        self.nexx = BugReport(bug, None, self)
        return self.nexx

    def __str__(self):
        return self.bug.__str__()
