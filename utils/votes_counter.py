#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import json
import base64

import sys

import datetime

# converts python unicode type strings inside dictionary to vanila string types
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class VotesCounter:
    def __init__(self):
        pass

    def count(self, journalString):
        results = {}

        journal = json.loads(journalString)
        del journalString

        def process_record(record):
            """
            Process single journal record
            :param record:
            :return: nothing, all results is a side effect in 'results' variable
            """
            for fingerprint in record['fingerprints']:
                decoded_metadata = json.loads(base64.b64decode(fingerprint['metadata']))
                if not decoded_metadata.__contains__('vote'):
                    continue
                vote = decoded_metadata['vote']
                for answer in vote['answers']:
                    question_title = answer['question']['title']
                    question_result = results.get(question_title,None)
                    if (question_result == None): question_result = {}; results[question_title]=question_result;
                    for key, answer in answer['vote'].items():
                        question_result[key]=question_result.get(key,0)+answer

        # Single thread processing
        for record in journal['records']:
            process_record(record)

        report = {}
        report['date'] = str(datetime.date.today())
        if journal.__contains__('timestamps'):
            if journal['timestamps'][0].__contains__('proof'):
                report['hash'] = journal['timestamps']['proof']['root']
            report['txid'] = journal['timestamps'][0]['txid']
        report['questions'] = results

        del journal
        #print(json.dumps(report, sort_keys=False, encoding="UTF-8", indent=4, separators=(',',': '), ensure_ascii=False))

        return byteify(report)

if __name__ == '__main__':
    journalString = open(sys.argv[1],'r').read()
    VotesCounter().count(journalString)
