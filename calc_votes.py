#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>
import json
import logging

from faker import Factory
from ledger_api import LedgerApi

class VotesCalculator:

    def __init__(self, baseUrl):
        self.logger = logging.getLogger(__name__)
        self.ledgerApi = LedgerApi(baseUrl)

    def getVoteResults(self, email, password, journalId):
        auth = self.ledgerApi.authenticateUser(email, password)
        journalJson = self.ledgerApi.getJournal(auth, journalId)

        #TODO

        return True

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)

    calculator = VotesCalculator()
    calculator.getVoteResults()
