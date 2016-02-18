#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

"""

To run tests:
    $ cd acronis-nrd-scripts
    $ python -m tests.publish_results_tests

"""

import unittest
import datetime
import logging
import json

from base64 import b64encode
from faker import Factory
from ConfigParser import SafeConfigParser

from utils.votes_counter import VotesCounter
from utils.ledger_api import LedgerApi

faker = Factory.create()

class TestVotesCounter(unittest.TestCase):
    def setUp(self):
        pass

    def test_votes_counter(self):
        with open('tests/resources/journal_template.json','r') as journal_template_file:
            journal_template = journal_template_file.read()
        with open('tests/resources/journal_record_template.json','r') as record_template_file:
            record_template = record_template_file.read()
        with open('tests/resources/vote_template.json','r') as vote_template_file:
            vote_template = vote_template_file.read()

        vote = vote_template
        voteBase64 = b64encode(vote)

        record = record_template % voteBase64

        voters_number = 1000
        records = (record+",")*(voters_number-1)+record

        journal = journal_template % records
        del records

        expected = {
            "date": str(datetime.date.today()),
            "questions": {
                "Утверждение итогов работы компании": {
                    "воздержался": voters_number,
                    "не голосовал": 0,
                    "да": 0,
                    "нет": 0
                },
                "Выбор нового председателя": {
                    "Иванов": 5*voters_number,
                    "Петров": 6*voters_number,
                    "воздержался": 0,
                    "Сидоров": voters_number,
                    "не голосовал": 0
                }
            },
            "txid": "74dc7d0cadf60bbb1d06a99f41db7b0a4e620d4c66cdc020729796e6fd0b8260"
        }

        result = VotesCounter().count(journal)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
