#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Igor Barinov <igorbarinov@me.com>

from locust import HttpLocust, TaskSet, task
import requests
from ConfigParser import SafeConfigParser
import datetime
import pickle
import uuid
import hashlib
import json
import base64
from Crypto.Hash import SHA256

# setup loggging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load configuration
parser = SafeConfigParser()
parser.read('load.ini')
AL_JOURNAL = parser.get('general', 'journal')
AL_HOST = parser.get('general', 'host')
AL_AUTH = parser.get('general','auth')
SIGNED_VOTES = 'data/signed_votes.p'


"""
Run this script in standalone mode
locust --host=http://167.114.247.67:8080
or use it as master node. You have to
locust  --master-host=167.114.247.67:8080
or use it as slave and connect to a master
locust  --slave --master-host=167.114.247.67:8080
"""



class UserBehavior(TaskSet):
    def on_start(self):
        self.i = 0

        logger.info('Loading signed votes..')
        self.signed_votes = pickle.load(open(SIGNED_VOTES,'rb'))
        self.max = len(self.signed_votes)

        """ on_start is called when a Locust start before any task is scheduled """
        self.client.headers = {"Authorization":AL_AUTH,'Content-Type':'application/json'}
        self.s = requests.Session()
        self.s.headers.update({'Authorization': AL_AUTH, 'Content-Type':'application/json'})

    # weight for task in ()
    @task(1)
    def timestamp(self):
        self.s.post(AL_HOST+'/api/journals/' + AL_JOURNAL +'/timestamp')
        print "timestamp journal " + str(datetime.datetime.now())

    @task(100)
    def create_record(self):
        logger.info('Creating a new record..')
        r = self.client.post("/api/records", '{}')

        if self.i > self.max:
            self.i = 0

        self.vote = self.signed_votes[self.i]

        # add fingerprint
        record_id = r.json()['id']
        logger.info('Adding new fingerprint..')
        self.s.post(AL_HOST + "/api/records/" + record_id + "/fingerprints", json.dumps({"metadata": base64.b64encode(json.dumps(self.vote)),
                                                                                         "metadataContentType":"application/json;enc=v1",
                                                                                         "metadataHash": hashlib.sha256(json.dumps(self.vote)).hexdigest(),
                                                                                         "nonce": base64.b64encode(str(uuid.uuid4()))}))
        # commit the record to a journal
        logger.info('Commiting the record..')
        self.s.post(AL_HOST+'/api/journals/' + AL_JOURNAL + '/commit/' + record_id, '{}')
        logger.info('Finished adding a record')
        self.i += 1

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
