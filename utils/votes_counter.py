#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import json
import base64

import sys


class VotesCounter:
    def __init__(self):
        pass

    def count(self, journalString):
        # Implement voting calc map-reduce task here
        # May be should use Pool.map for this

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

        del journal

        print(json.dumps(results, sort_keys=True, encoding="UTF-8", indent=4, separators=(',',': ')))

        return results


if __name__ == '__main__':
    journalString = open(sys.argv[1],'r').read()
    VotesCounter().count(journalString)