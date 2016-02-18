# -*- coding: utf-8 -*-
# Acronis Ledger API client
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import json
import logging
import requests

from base64 import b64encode

class LedgerApi:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.headers = {
            'Content-Type': 'application/json'
        }

        self.logger = logging.getLogger(__name__)

    def dumpHttpResponse(self, response):
        self.logger.debug(response.status_code)
        self.logger.debug(response.headers)
        self.logger.debug(response.content)

    def createUser(self, email, password):
        self.logger.debug('Creating a user {email: "%s", password: "%s"}' % (email, password))

        res = requests.post(self.baseUrl + '/api/users', headers = self.headers,
            data =  '{"email": "%s", "password": "%s"}' % (email, password))
        res.raise_for_status()

        self.dumpHttpResponse(res)

        key = str(res.json()["accessTokens"][0]["accessKey"])
        secret = str(res.json()["accessTokens"][0]["accessSecret"])

        basicAuth = "Basic " + b64encode(key + ":" + secret).decode("ascii")

        self.logger.debug('Basic auth: ' + basicAuth)
        self.logger.debug('User was successfully created.')

        return basicAuth

    def authenticateUser(self, email, password):
        self.logger.info('Authenticating a user {email: "%s", password: "%s"}' % (email, password))

        res = requests.post(self.baseUrl + '/api/user/authentication', headers = self.headers,
            data = '{"password":"%s", "email": "%s"}' % (password, email))
        res.raise_for_status()

        self.dumpHttpResponse(res)

        key = str(res.json()["accessTokens"][0]["accessKey"])
        secret = str(res.json()["accessTokens"][0]["accessSecret"])

        basicAuth = "Basic " + b64encode(key + ":" + secret).decode("ascii")

        self.logger.debug('Basic auth: ' + basicAuth)
        self.logger.debug('User was successfully authenticated.')

        return basicAuth

    def getJournal(self, auth, journalId):
        headers = self.headers.copy()
        headers.update({ 'Authorization': auth })

        self.logger.debug('Retrieving a journal %s' % journalId)

        res = requests.get(self.baseUrl + '/api/journals/%s' % journalId, headers = headers)
        res.raise_for_status()

        self.dumpHttpResponse(res)
        self.logger.debug('Journal was successfully retrieved.')

        return res.content

    def createJournal(self, auth, journalName, journalType='blockchain_merkletree'):
        headers = self.headers.copy()
        headers.update({ 'Authorization': auth })

        self.logger.debug('Creating a journal with a name %s\n' % journalName)

        res = requests.post(self.baseUrl + '/api/journals', headers = headers,
            data =  '{"name": "%s", "type": "%s"}' % (journalName, journalType))
        res.raise_for_status()

        self.dumpHttpResponse(res)
        self.logger.debug('Journal was successfully created.')

        journalId = res.json()["id"]
        self.logger.debug('Journal id= ' + journalId)

        return journalId

    def timestampJournal(self, auth, journalId):
        headers = self.headers.copy()
        headers.update({ 'Authorization': auth })

        self.logger.debug('Creating a timestamp for journal %s' % journalId)

        res = requests.post(self.baseUrl + '/api/journals/%s/timestamp' % journalId, headers = headers,
            data =  '{}')
        res.raise_for_status()

        self.dumpHttpResponse(res)
        self.logger.debug('Timestamp was successfully created.')

    def createRecord(self, auth):
        headers = self.headers.copy()
        headers.update({ 'Authorization': auth })

        self.logger.debug('Creating a new record in ledger.')

        res = requests.post(self.baseUrl + '/api/records', headers = headers, data = "{}")
        res.raise_for_status()

        self.dumpHttpResponse(res)

        recordId = res.json()["id"]
        return recordId

    def saveRecordFingerprint(self, auth, recordId, jsonData):
        headers = self.headers.copy()
        headers.update({ 'Authorization': auth })

        self.logger.debug('Updating data for record with id= ' + recordId)

        res = requests.post(self.baseUrl + '/api/records/%s/fingerprints' % recordId, headers = headers, data = jsonData)
        res.raise_for_status()

        self.dumpHttpResponse(res)
        self.logger.debug('Record was successfully updated.')

    def commitRecord(self, auth, journalId, recordId):
        headers = self.headers.copy()
        headers.update({ 'Authorization': auth })

        self.logger.debug('Commiting a record %s to journal %s' % (recordId, journalId))

        res = requests.post(self.baseUrl + '/api/journals/%s/commit/%s' % (journalId, recordId), headers = headers, data = "{}")
        res.raise_for_status()

        self.dumpHttpResponse(res)
        self.logger.debug('Record was successfully commited to journal.')
