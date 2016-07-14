from libzilla.session import LibzillaSession
from libzilla.session import RESOLUTIONS
from libzilla.session import STATUSES
import sys
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
        self.args = args
        self.session = LibzillaSession(args)
        self.check_for_bug_numbers()

        args['<bug_number>'] = set(args['<bug_number>'])
        list_of_br = ', '.join(args['<bug_number>'])
        first_br = self.walk_list_of_br(args)

        self.prompt = '> '
        self.intro = INTRO.format(first_br, list_of_br)

    def walk_list_of_br(self, args):
        info = {
            '--resolution': args.get('--resolution'),
            '--comment': args.get('--comment'),
            '--status': args.get('--status')
        }
        bug_numbers = args['<bug_number>']
        first_br = bug_numbers.pop()
        first = last = BugReport(first_br, info)
        for bug_number in bug_numbers:
            last = last.add(bug_number, info)
        last.nexx = first
        first.previous = last
        self.current_br = first
        return first_br

    def check_for_bug_numbers(self):
        if not self.session.check_for_bug_numbers(self.args):
            sys.exit(1)

    def do_comment(self, line):
        """Add comment to current bug report."""
        if not line:
            print('Sorry, comment cannot be empty!')
            return
        comment = self.current_br.info.get('--comment')
        if comment:
            print('Comment was: {0}'.format(comment))
        else:
            print('There was no comment set.')
        self.current_br.info['--comment'] = line
        print('Comment is now: {0}'.format(line))

    def do_status(self, line):
        """Set STATUS to current bug report."""
        if not line:
            print('Sorry, STATUS cannot be empty!')
            return
        if not self.session.check_for_status(line):
            return
        status = self.current_br.info.get('--status')
        if status:
            print('STATUS was: {0}'.format(status))
        else:
            print('There was no STATUS set.')
        self.current_br.info['--status'] = line
        print('STATUS is now: {0}'.format(line))

    def complete_status(self, text, line, start_index, end_index):
        """Complete status command."""
        if text:
            return [status for status in STATUSES if status.startswith(text)]
        else:
            return STATUSES

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
        if not self.session.check_for_resolution(line):
            return
        resolution = self.current_br.info.get('--resolution')
        if resolution:
            print('RESOLUTION was: {0}'.format(resolution))
        else:
            print('There was no RESOLUTION set.')
        self.current_br.info['--resolution'] = line
        print('RESOLUTION is now: {0}'.format(line))

    def do_current(self, line):
        """Print current bug report information."""
        print(self.current_br)

    def do_query(self, line):
        """Query Bugzilla about current bug report i.e. status, \
resolution and summary."""
        self.session.connect()
        self.session.get_bug_info(self.current_br.bug_number)

    def do_update(self, line):
        """Update current bug report."""
        self.session.connect()
        update = dict(self.current_br.info)
        update['<bug_number>'] = [self.current_br.bug_number]
        self.session.process_bug_numbers(update)
        self.session.update_bugs()

    def do_next(self, line):
        """Switch to next bug report in the stack."""
        self.current_br = self.current_br.nexx
        print('Switch to next bug report: {0}'
              .format(self.current_br.bug_number))

    def do_previous(self, line):
        """Switch to previous bug report in the stack."""
        self.current_br = self.current_br.previous
        print('Switch to previous bug report: {0}'
              .format(self.current_br.bug_number))

    def do_EOF(self, line):
        """Quit shell by pressing ^D."""
        print('Bye!')
        return -1

    def do_quit(self, line):
        """Quit shell."""
        return self.do_EOF(line)


class BugReport:
    def __init__(self, bug_number, info, nexx=None, previous=None):
        self.info = info
        self.bug_number = bug_number

        self.nexx = nexx
        self.previous = previous

    def add(self, bug_number, info):
        self.nexx = BugReport(bug_number, info, None, self)
        return self.nexx

    def __str__(self):
        my_str = 'Bug #: %s' % (self.bug_number)
        for key, val in self.info.items():
            key = key.replace('--', '')
            if key == 'comment': key = key.capitalize()
            else: key = key.upper()
            print(key)
            my_str = '{0}\n[{1}: {2}]'.format(
                my_str, key, val
            )
        return my_str
