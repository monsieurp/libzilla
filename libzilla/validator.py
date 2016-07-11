from libzilla.exceptions import LibZillaException
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

"""This module contains a sole class for validating an URL."""

def validate_url(url):
    if not url:
        raise LibZillaException('URL is empty!')

    outurl = urlparse(url)
    scheme, base, path = outurl[0:3]
    if not scheme and not base and path:
        base = path
        path = ''

    if not scheme or not scheme.startswith('https'):
        logger.info("HTTPS scheme not detected!")
        logger.info("Defaulting scheme to 'https'.")
        scheme = 'https'

    if 'rest' not in path:
        logger.info('URL must point to the Bugzilla REST API!')
        logger.info("Defaulting path to 'rest'.")
        path = '/rest'

    if not base or not path:
        raise LibZillaException('Malformed URL! \"{0}\"'.format(url))

    valid_url = '%s://%s%s' % (scheme, base, path)
    logger.info('Validated URL: {0}'.format(valid_url))

    return valid_url
