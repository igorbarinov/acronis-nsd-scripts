#!/usr/bin/env python

import logging

from ConfigParser import SafeConfigParser
from utils.ledger_api import LedgerApi

# setup loggging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = SafeConfigParser()
parser.read('load.ini')

baseUrl = parser.get('general', 'host')
journal = parser.get('general', 'journal')
username = parser.get('general', 'username')
password = parser.get('general', 'password')

ledgerApi = LedgerApi(baseUrl)

session = ledgerApi.authenticateUser(username, password)

ledgerApi.timestampJournal(session, journal)
