#!/usr/bin/env python
# Author: Igor Barinov <igorbarinov@me.com>

import sys, os
import requests
import logging

from requests.auth import HTTPBasicAuth
from ConfigParser import SafeConfigParser
from faker import Factory
from base64 import b64encode
from utils.ledger_api import LedgerApi

# setup loggging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

faker = Factory.create()

parser = SafeConfigParser()
parser.read('load.ini')

baseUrl = parser.get('general', 'host')

ledgerApi = LedgerApi(baseUrl)

"""

Create user

"""

# TODO implement click
# import click
# @click.command()
# @click.option('--timestamp-weight', default=1, help='Weight of a timestamp operation')

logger.debug('Starting creating an user')

username = faker.email()
password = "password"

AL_AUTH = ledgerApi.createUser(username, password)

# save user info to config
parser.set('general', 'auth', AL_AUTH)
parser.set('general', 'username', username)
parser.set('general', 'password', password)

logger.debug('User created.')

"""

Create journal

"""

logger.debug('Starting creating a journal')

AL_JOURNAL = ledgerApi.createJournal(AL_AUTH, faker.name())

# save journal info to cinfig
parser.set('general', 'journal', AL_JOURNAL)

logger.debug('Journal created.')

# Saving configuration
with open('load.ini', 'w') as configfile:
    parser.write(configfile)
