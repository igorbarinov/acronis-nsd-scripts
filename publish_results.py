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
from quik import FileLoader

logging.basicConfig(level = logging.INFO)

# Load configuration params
parser = SafeConfigParser()
parser.read('load.ini')

baseUrl = parser.get('general', 'host')
journalId = parser.get('general', 'journal')
username = parser.get('general', 'username')
password = parser.get('general', 'password')

raw_path = parser.get('reporting', 'raw_export_path')
html_path = parser.get('reporting', 'html_export_path')
html_template_path = parser.get('reporting', 'html_template')

def publish_results(username, password, journalId):
    # Initialize Ledger API
    ledgerApi = LedgerApi(baseUrl)

    # Authenticate user in ledger
    session = ledgerApi.authenticateUser(username, password)

    # Retrieve voting journal data
    journalString = ledgerApi.getJournal(session, journalId)
    export_raw(journalString)

    # Calculate voting results
    votingResults = VotesCounter().count(journalString)

    # Export result to html presentation
    html = generate_html(votingResults)
    export_html(html)

def export_raw(journalString):
    filename = 'journal.json'
    export_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), raw_path, filename)

    with open(export_path, 'w') as json_file:
        json_file.write(journalString)

def generate_html(votingResults):
    # Load html template for rendering
    template = FileLoader("").load_template(html_template_path)

    # Render voting results data
    html = template.render(votingResults)

    return html

def export_html(html):
    filename = 'index.html'
    export_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), html_path, filename)

    with open(export_path, 'w') as text_file:
        text_file.write(html)

if __name__ == '__main__':
    # Retrieve and publish voting results
    publish_results(username, password, journalId)
