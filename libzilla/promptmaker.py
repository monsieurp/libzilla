import libzilla.validator as validator
import getpass
import logging
import re
import sys

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

"""This module helps create prompts for asking user for information."""


def prompt(prompt_msg):
    """Create a prompt using prompt_msg.
    :param prompt_msg: Message to display to user.
    """
    while True:
        try:
            answer = input(prompt_msg)
        except (EOFError, KeyboardInterrupt):
            logger.fatal("Bailing out...\n")
            sys.exit(1)

        if re.search(r'\w+', answer):
            return answer
        else:
            sys.stderr.write("Please provide an answer.\n")


def prompt_for_credentials(credentials):
    """Create a prompt to ask user for credentials.
    :param credentials: a dictionary to store credentials into.
    """
    while True:
        credentials['url'] = prompt('Bugzilla URL: ')
        credentials['username'] = prompt('Username: ')
        credentials['password'] = getpass.getpass()
        print("OK! Let's recap.")
        for item in credentials.keys():
            itm = item.capitalize()
            if item == 'url':
                itm = item.upper()

            to_print = '%s: %s' % (itm, credentials[item])
            if item == 'password':
                # Don't echo back password
                to_print = '%s: %s' % (itm, '*' * len(str(credentials[item])))
            print(to_print)

        if prompt('Are these settings correct? [y/n] ') == 'y':
            credentials['url'] = validator.validate_url(credentials['url'])
            break
    return credentials
