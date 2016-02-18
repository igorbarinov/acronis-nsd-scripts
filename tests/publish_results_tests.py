#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

"""

To run tests:
    $ cd acronis-nrd-scripts
    $ python -m tests.publish_results_tests

"""

import unittest
import logging

from base64 import b64encode
import datetime
from faker import Factory
from ConfigParser import SafeConfigParser

from publish_results import publish_results
from publish_results import generate_html
from publish_results import export_raw
from publish_results import export_html
from utils.ledger_api import LedgerApi

faker = Factory.create()

class TestResultPublisher(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)

        # Load ledger base url from configuration
        parser = SafeConfigParser()
        parser.read('load.ini')
        baseUrl = parser.get('general', 'host')

        # Initialize ledger api client
        self.ledgerApi = LedgerApi(baseUrl)

        with open('tests/resources/fingerprint_template.json','r') as fingerprint_template_file:
            fingerprint_template = fingerprint_template_file.read()
        with open('tests/resources/vote_template.json','r') as vote_template_file:
            vote_template = vote_template_file.read()

        voteBase64 = b64encode(vote_template)

        self.testFingerprint = fingerprint_template % voteBase64

        self.username = faker.email()
        self.password = "nq5YxjWKxhQABvYa"
        self.journalId = self.setupJournal(self.username, self.password)

    def setupJournal(self, username, password):
        session = self.ledgerApi.createUser(username, password)

        journalId = self.ledgerApi.createJournal(session, faker.name())

        recordId = self.ledgerApi.createRecord(session)
        self.ledgerApi.saveRecordFingerprint(session, recordId, self.testFingerprint)
        self.ledgerApi.commitRecord(session, journalId, recordId)

        # Uncomment next line if need to timestamp (create a transaction in blockchain)
        self.ledgerApi.timestampJournal(session, journalId)

        return journalId

    def test_publish_results(self):
        publish_results(self.username, self.password, self.journalId)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
