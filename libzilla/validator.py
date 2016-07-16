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
