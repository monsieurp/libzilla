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

import subprocess
import re

"""A set of useful functions when dealing with git."""


def look_for_bug_numbers(line, candidates):
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
