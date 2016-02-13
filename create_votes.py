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

# setup loggging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# and progressbar
from tqdm import *

random_generator = Random.new().read

"""

This script generates votes for number of users defined in
NUMBER_OF_VOTES constant.

"""
PRIVATE_KEY_FILE = 'data/private_keys.p'
NUMBER_OF_VOTES = 10000
 = ""
REPORT_SHA2 = ""

# mock data

reports = [{REPORT_URL:"http://www.gazprom.ru/f/posts/05/298369/gazprom-annual-report-2014-ru.pdf", REPORT_SHA2:"959ca7b22af7725d7370ded13d3a3f53b3b2ff953a3f6267075438e141ee4525"]
decision = [{u'да': True, u'нет': False, u'воздержался': False, u'не голосовал': False},
{u'да': False, u'нет': True, u'воздержался': False, u'не голосовал': False},
{u'да': False, u'нет': False, u'воздержался': True, u'не голосовал': False},
{u'да': False, u'нет': False, u'воздержался': False, u'не голосовал': True}]

def create_votes(votes):

    questions = {}
    for i in tqdm(range(1,votes+1)):
        # question one
        questions['questions'] = []
        questions['questions'].append({"REPORT_URL": REPORT_URL , "REPORT_SHA2": REPORT_SHA2, "vote": []})
        questions['questions'][0]['vote'].append(random.choice(decision))
        #sign
        private_key = RSA.importKey(private_keys[i])
        hash = SHA256.new(json.dumps(questions))
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(hash)
        logger.debug({"vote": json.dumps(questions), "signature":signature, "user_id":i})

if __name__ == '__main__':
    private_keys = pickle.load(open(PRIVATE_KEY_FILE,'rb'))

    create_votes(NUMBER_OF_VOTES)
