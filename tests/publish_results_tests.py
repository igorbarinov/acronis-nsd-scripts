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
from faker import Factory
from ConfigParser import SafeConfigParser

from publish_results import publish_results
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

        voteJson = """{
            "voter": {
                "id": "b2ff953a3f6267"
            },
            "answers": [
                {
                    "question": {
                        "id": "1",
                        "title": "Утверждение итогов работы компании",
                        "files": [
                            {
                                "file_title": "Годовойотчёт",
                                "file_url": "http://www.gazprom.ru/f/posts/05/298369/gazprom-annual-report-2014-ru.pdf",
                                "file_sha2": "959ca7b22af7725d7370ded13d3a3f53b3b2ff953a3f6267075438e141ee4525"
                            }
                        ]
                    },
                    "vote": {
                        "да": "false",
                        "нет": "false",
                        "воздержался": "true",
                        "не голосовал": "false"
                    }
                },
                {
                    "question": {
                        "id": "1",
                        "title": "Выбор нового председателя"
                    },
                    "vote": {
                        "Иванов": 5,
                        "Сидоров": 1,
                        "Петров": 6,
                        "воздержался": false,
                        "не голосовал": false
                    }
                }
            ]
        }"""

        voteBase64 = b64encode(voteJson)

        self.testRecordData = """{
            "nonce": [],
            "metadata": "%s",
            "metadataContentType": "application/json;enc=v1",
            "metadataHash": []
        }""" % voteBase64

        self.username = faker.email()
        self.password = "nq5YxjWKxhQABvYa"
        self.journalId = self.setupJournal(self.username, self.password)

    def setupJournal(self, username, password):
        session = self.ledgerApi.createUser(username, password)

        journalId = self.ledgerApi.createJournal(session, faker.name())

        recordId = self.ledgerApi.createRecord(session)
        self.ledgerApi.saveRecordData(session, recordId, self.testRecordData)
        self.ledgerApi.commitRecord(session, journalId, recordId)

        # Uncomment next line if need to timestamp (create a transaction in blockchain)
        #self.ledgerApi.timestampJournal(session, journalId)

        return journalId

    def test_raw_result_saved(self):
        publish_results(self.username, self.password, self.journalId)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
