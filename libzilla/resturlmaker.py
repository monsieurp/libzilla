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

from string import Template

"""The RESTURLMaker class helps build URLs for the Bugzilla REST API."""


class RESTURLMaker:
    def __init__(self, url=''):
        self.url = url
        self.token = ''

    def make_login_url(self, username='', password=''):
        return Template('$url/login?login=$username&password=$password').substitute(
            url=self.url,
            username=username,
            password=password
        )

    def make_bug_url(self, bug_number=''):
        return Template('$url/bug/$bug_number').substitute(
            url=self.url,
            bug_number=bug_number
        )

    def make_new_bug_url(self):
        return Template('$url/bug').substitute(
            url=self.url
        )
