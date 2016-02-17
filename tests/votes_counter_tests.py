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
        vote = """
        {
            "voter": {
                "id": "5d7370ded13d"
            },
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
                        "да": false,
                        "нет": false,
                        "воздержался": true,
                        "не голосовал": false
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
        }
        """

        voteBase64 = b64encode(vote)

        record = """
                       {
                    "id": "b3749f23-d9f2-401e-91ca-673956a79066",
                    "fingerprints": [
                        {
                            "metadata": "%s",
                            "metadataContentType": "application/json;enc=v1",
                            "metadataHash": "",
                            "nonce": ""
                        }
                    ],
                    "timestamps": [
                        {
                            "txid": "74dc7d0cadf60bbb1d06a99f41db7b0a4e620d4c66cdc020729796e6fd0b8260",
                            "proof": {
                                "sequence": [
                                    {
                                        "hash": "EbZNktUdzgMDfwqWFVWigHT7Ca66RqX3wan2seVRP2w=",
                                        "direction": "RIGHT"
                                    }
                                ],
                                "op_return": "df4fff68d8ce5c0ee72b7fb3f28c41b12da96d50e1f08474133c5b1ab63e71253e0d1d25ceaafaf3",
                                "root": "K1dJGN8tpUnI4bwLdntgpRjkLnsO/CRcbNy3Y6eAlTo=",
                                "fingerprint_ripemd160": "30//aNjOXA7nK3+z8oxBsS2pbVA=",
                                "nonce": "4fCEdBM8Wxq2PnElPg0dJc6q+vM="
                            },
                            "fingerprint": "yZxkSpLS8sTyqocIqPbaqFXIDqQ=",
                            "nonce": "4fCEdBM8Wxq2PnElPg0dJc6q+vM="
                        }
                    ],
                    "files": [],
                    "fingerprint": "oPRo+QHEkeA2ewxIaOV6WYveGsg=",
                    "nonce": "nIADOspyC8QnHiC9Nr8PnvP18OY="
                }
        """ % voteBase64

        records = (record+",")*5+record

        journal = """
        {
            "id": "5b9a74e9-52e0-4727-82a6-6b7286f6bcd3",
            "type": "blockchain_merkletree",
            "name": "Ernesto O'Connell",
            "records": [
                %s
            ],
            "timestamps": [
                {
                    "txid": "74dc7d0cadf60bbb1d06a99f41db7b0a4e620d4c66cdc020729796e6fd0b8260"
                }
            ]
        }
        """ % records

        expected = json.loads("""{
            "\u0412\u044b\u0431\u043e\u0440 \u043d\u043e\u0432\u043e\u0433\u043e \u043f\u0440\u0435\u0434\u0441\u0435\u0434\u0430\u0442\u0435\u043b\u044f": {
                "\u0418\u0432\u0430\u043d\u043e\u0432": 30,
                "\u041f\u0435\u0442\u0440\u043e\u0432": 36,
                "\u0421\u0438\u0434\u043e\u0440\u043e\u0432": 6,
                "\u0432\u043e\u0437\u0434\u0435\u0440\u0436\u0430\u043b\u0441\u044f": 0,
                "\u043d\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b": 0
            },
            "\u0423\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u0438\u0442\u043e\u0433\u043e\u0432 \u0440\u0430\u0431\u043e\u0442\u044b \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438": {
                "\u0432\u043e\u0437\u0434\u0435\u0440\u0436\u0430\u043b\u0441\u044f": 6,
                "\u0434\u0430": 0,
                "\u043d\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b": 0,
                "\u043d\u0435\u0442": 0
            }
        }""")

        result = VotesCounter().count(journal)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
