#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Igor Barinov <igorbarinov@me.com>

import cPickle as pickle
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
import Crypto.Util.number as CUN
import os
import json
import random
import pprint
import base64
import gzip


# setup loggging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# and progressbar
from tqdm import *

random_generator = Random.new().read

"""

This script generates votes for number of users defined in
NUMBER_OF_VOTES constant.

"""
PRIVATE_KEY_FILE = 'data/private_keys.p'
NUMBER_OF_VOTES = 100000

# mock data

reports = [{u"REPORT_URL":u"http://www.gazprom.ru/f/posts/05/298369/gazprom-annual-report-2014-ru.pdf",
            u"REPORT_SHA2":u"959ca7b22af7725d7370ded13d3a3f53b3b2ff953a3f6267075438e141ee4525"}]

decision = [{u'да': True, u'нет': False, u'воздержался': False, u'не голосовал': False},
{u'да': False, u'нет': True, u'воздержался': False, u'не голосовал': False},
{u'да': False, u'нет': False, u'воздержался': True, u'не голосовал': False},
{u'да': False, u'нет': False, u'воздержался': False, u'не голосовал': True}]

boolean = [True,False]

votes = []


def save_zipped_pickle(obj, filename, protocol=-1):
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol)

def create_vote(i):
    return {
            u"voter": {
               u"id": i
            },
            u"answers": [
                {
                    u"question": {
                        u"id": u"1",
                        u"type": u"YesNo",
                        u"title": u"Утверждение итогов работы компании",
                        u"files": [
                            {
                                u"file_title": u"Годовойотчёт",
                                u"file_url": u"http://www.gazprom.ru/f/posts/05/298369/gazprom-annual-report-2014-ru.pdf",
                                u"file_sha2": u"959ca7b22af7725d7370ded13d3a3f53b3b2ff953a3f6267075438e141ee4525"
                            }
                        ]
                    },
                    u"vote": random.choice(decision)
                },
                {
                    u"question": {
        u"id": u"2",
                       u"type": u"CandidatVotes",
                        u"title": u"Выбор нового председателя"
                    },
                    u"vote": {
                        u"Иванов": random.randint(1,9),
                        u"Сидоров": random.randint(1,9),
                        u"Петров": random.randint(1,9),
                        u"воздержался": random.choice(boolean) ,
                        u"не голосовал": random.choice(boolean)
                    }
                }
            ]
        }

def create_votes(votes):
    signed_votes = []
    for i in tqdm(range(1,votes+1)):
        vote = create_vote(i)
        private_key = RSA.importKey(private_keys[i])
        hash = SHA256.new(json.dumps(vote))
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(hash)
        signed_votes.append({u"vote": json.dumps(vote), u"base64_signature":base64.b64encode(signature), u"user_id":i})

    save_zipped_pickle(signed_votes,'data/signed_votes.p.gz')

if __name__ == '__main__':
    logger.info('Start loading keys...')
    private_keys = pickle.load(open(PRIVATE_KEY_FILE,'rb'))
    logger.info('End loading keys...')
    # debug
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(create_vote(1))
    create_votes(NUMBER_OF_VOTES)
    logger.info('Bye')
