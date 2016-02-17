#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import os
import json
import logging

from datetime import datetime

from utils.ledger_api import LedgerApi
from utils.votes_counter import VotesCounter
from ConfigParser import SafeConfigParser

logging.basicConfig(level = logging.DEBUG)

# Load configuration params
parser = SafeConfigParser()
parser.read('load.ini')

baseUrl = parser.get('general', 'host')
journalId = parser.get('general', 'journal')
username = parser.get('general', 'username')
password = parser.get('general', 'password')
raw_path = parser.get('reporting', 'raw_path')
html_path = parser.get('reporting', 'html_path')

def publish_results(username, password, journalId):
    # Initialize Ledger API
    ledgerApi = LedgerApi(baseUrl)

    # Authenticate user in ledger
    session = ledgerApi.authenticateUser(username, password)

    # Retrieve voting journal data
    journal = ledgerApi.getJournal(session, journalId)
    export_raw(journal)

    # Calculate voting results
    results = VotesCounter().count(journal)

    # Export result to html presentation
    html = generate_html(results)
    export_html(html)

def export_raw(journal):
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.json'
    export_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), raw_path, filename)

    with open(export_path, 'w') as json_file:
        json.dump(journal, json_file)

def generate_html(results):
    #TODO html template code here
    return "<html></html>"

def export_html(html):
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.html'
    export_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), html_path, filename)

    with open(export_path, 'w') as text_file:
        text_file.write(html)

if __name__ == '__main__':
    # Retrieve and publish voting results
    publish_results(username, password, journalId)
