#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import unittest
import logging

from base64 import b64encode
from faker import Factory
from calc_votes import VotesCalculator
from ledger_api import LedgerApi
from ConfigParser import SafeConfigParser

faker = Factory.create()

class TestVotesCalculator(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)

        parser = SafeConfigParser()
        parser.read('load.ini')
        baseUrl = parser.get('general', 'host')

        self.ledgerApi = LedgerApi(baseUrl)
        self.votesCalculator = VotesCalculator(baseUrl)

        voteJson = """{
            "answers": [
                {
                    "question": {
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

    def test_journal_is_saving(self):
        email = faker.email()
        password = "nq5YxjWKxhQABvYa"
        auth = self.ledgerApi.createUser(email, password)

        journalId = self.ledgerApi.createJournal(auth, faker.name())
        recordId = self.ledgerApi.createRecord(auth)
        self.ledgerApi.saveRecordData(auth, recordId, self.testRecordData)
        self.ledgerApi.commitRecord(auth, journalId, recordId)

        # Don't waste the money
        #self.ledgerApi.timestampJournal(auth, journalId)

        result = self.votesCalculator.getVoteResults(email, password, journalId)
        self.assertTrue(result)

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    unittest.main()
