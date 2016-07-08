import subprocess
import re


def look_for_bug_numbers(line):
    candidates = (
        r'^.*?Fixes bug (\d+).*?$',
        r'^.*?Fixes security bug (\d+).*?$',
        r'^\s+Gentoo-Bug:(\s+\d+)$',
        r'^\s+Gentoo-Bug:\s?https://bugs.gentoo.org/(\d+)'
    )

    for candidate in candidates:
        match = re.search(candidate, line)
        if match:
            return match.group(1).strip()


def run_command(cmd):
    out = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]
    out = out.decode('utf8')
    out = out.split('\n')[:-1]
    return out


def trim_spaces(commit):
    body = ''
    for line in iter(commit):
        line = line.strip() + '\n'
        body = body + line
    return body.strip()
