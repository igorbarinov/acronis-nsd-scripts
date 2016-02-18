#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

"""
Testing Ledger client API

To run tests:
    $ cd acronis-nrd-scripts
    $ python -m tests.ledger_api_tests

"""

import unittest
import logging

from base64 import b64encode
import datetime
from faker import Factory
from ConfigParser import SafeConfigParser

from utils.ledger_api import LedgerApi

faker = Factory.create()

class TestLedgerApi(unittest.TestCase):
    def test_all(self):
        logger = logging.getLogger(__name__)

        # Load ledger base url from configuration
        parser = SafeConfigParser()
        parser.read('load.ini')

        baseUrl = parser.get('general', 'host')
        username = parser.get('general', 'username')
        password = parser.get('general', 'password')

        # Initialize ledger api client
        ledgerApi = LedgerApi(baseUrl)

        with open('tests/resources/fingerprint_template.json', 'r') as fingerprint_template_file:
            fingerprint_template = fingerprint_template_file.read()
        with open('tests/resources/vote_template.json', 'r') as vote_template_file:
            vote_template = vote_template_file.read()

        vote = vote_template
        voteBase64 = b64encode(vote)

        fingerprint = fingerprint_template % voteBase64

        session = ledgerApi.authenticateUser(username, password)

        journalId = ledgerApi.createJournal(session, faker.name())

        recordId = ledgerApi.createRecord(session)

        ledgerApi.saveRecordFingerprint(session, recordId, fingerprint)
        ledgerApi.commitRecord(session, journalId, recordId)

        # Uncomment next line if need to timestamp (create a transaction in blockchain)
        ledgerApi.timestampJournal(session, journalId)

        print journalId

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
