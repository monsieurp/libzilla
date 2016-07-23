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

from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

"""This module contains a sole class for validating an URL."""


def validate_url(url):
    """Validate an URL according to the Bugzilla REST API and how it is exposed
    to the outside world. The Bugzilla REST API is described in the following
    Wiki document: https://wiki.mozilla.org/Bugzilla:REST_API.
    url: URL to validate."""

    if not url:
        import sys
        logger.error('The URL provided is empty!')
        sys.exit(1)

    outurl = urlparse(url)
    scheme, base, path = outurl[0:3]

    if not scheme or not scheme.startswith('https'):
        logger.info("HTTPS scheme not detected!")
        logger.info("Defaulting scheme to 'https'.")
        scheme = 'https'

    if not base and path:
        base = path
        path = ''

    if 'rest' not in path:
        logger.info('URL must point to the REST API!')
        logger.info("Defaulting path to 'rest'.")
        path = '/rest'

    valid_url = '%s://%s%s' % (scheme, base, path)
    logger.info('Validated URL: {0}'.format(valid_url))

    return valid_url
