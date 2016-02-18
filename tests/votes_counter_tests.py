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

    def test_six_vote(self):
        with open('resources/journal_template.json','r') as journal_template_file:
            journal_template = journal_template_file.read()
        with open('resources/journal_record_template.json','r') as record_template_file:
            record_template = record_template_file.read()
        with open('resources/record_vote_template.json','r') as vote_template_file:
            vote_template = vote_template_file.read()

        vote = vote_template
        voteBase64 = b64encode(vote)

        record = record_template % voteBase64

        voters_number = 100000
        records = (record+",")*(voters_number-1)+record

        journal = journal_template % records

        expected = json.loads("""{
            "Выбор нового председателя": {
                "\u0418\u0432\u0430\u043d\u043e\u0432": """+str(5*voters_number)+""",
                "\u041f\u0435\u0442\u0440\u043e\u0432": """+str(6*voters_number)+""",
                "\u0421\u0438\u0434\u043e\u0440\u043e\u0432": """+str(voters_number)+""",
                "\u0432\u043e\u0437\u0434\u0435\u0440\u0436\u0430\u043b\u0441\u044f": 0,
                "\u043d\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b": 0
            },
            "\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0438\u0442\u043e\u0433\u043e\u0432 \u0440\u0430\u0431\u043e\u0442\u044b \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438": {
                "\u0432\u043e\u0437\u0434\u0435\u0440\u0436\u0430\u043b\u0441\u044f": """+str(voters_number)+""",
                "\u0434\u0430": 0,
                "\u043d\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b": 0,
                "\u043d\u0435\u0442": 0
            }
        }""")

        result = VotesCounter().count(journal)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
