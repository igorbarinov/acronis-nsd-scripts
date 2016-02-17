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

from utils.votes_counter import VotesCounter
from utils.ledger_api import LedgerApi


faker = Factory.create()

class TestVotesCounter(unittest.TestCase):
    def setUp(self):
        pass

    def test_one_vote(self):
        vote = """
        {
            "voter": {
                "id": "5d7370ded13d"
            }
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

        journal = """
        {
            "id": "5b9a74e9-52e0-4727-82a6-6b7286f6bcd3",
            "type": "blockchain_merkletree",
            "name": "Ernesto O'Connell",
            "records": [
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
                },
                {
                    "id": "eb07c643-d62f-46bc-bfbc-11f158076136",
                    "fingerprints": [
                        {
                            "metadata": "eyJoYXNoIjoiSzFkSkdOOHRwVW5JNGJ3TGRudGdwUmprTG5zTy9DUmNiTnkzWTZlQWxUbz0iLCJoYXNoQWxnb3JpdGhtIjoiU0hBXzI2NSIsInByb3BlcnRpZXMiOnsidHlwZSI6ImNvbS5hY3JvbmlzLmxlZGdlci5jaGFpbiJ9fQ==",
                            "metadataContentType": "application/json;v=1",
                            "metadataHash": "kl0xSzb+Xwr7uKirW1TjIyPmP6C27Gtl6BCFtEFhlP4=",
                            "nonce": "4fCEdBM8Wxq2PnElPg0dJc6q+vM="
                        }
                    ],
                    "timestamps": [],
                    "files": [],
                    "fingerprint": "xbILEYgJcKwk1Hs27+Q0VWkamqM=",
                    "nonce": "nIADOspyC8QnHiC9Nr8PnvP18OY="
                }
            ],
            "timestamps": [
                {
                    "txid": "74dc7d0cadf60bbb1d06a99f41db7b0a4e620d4c66cdc020729796e6fd0b8260"
                }
            ]
        }
        """ % voteBase64

        expected = {
            "txid": "74dc7d0cadf60bbb1d06a99f41db7b0a4e620d4c66cdc020729796e6fd0b8260"
        }

        result = VotesCounter().count(journal)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
