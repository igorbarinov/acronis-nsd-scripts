#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import json
import base64
import time
import multiprocessing

def f(record):
    for fingerprint in record['fingerprints']:
        vote = json.loads(base64.b64decode(fingerprint['metadata']))
        for answer in vote['answers']:
            question_title = answer['question']['title']
            question_result = None #results.get(question_title,None)
            if (question_result == None): question_result = {}; #results[question_title]=question_result;
            for key, answer in answer['vote'].items():
                question_result[key]=question_result.get(key,0)+answer

def process_record(record, results):
    """
    Process single jpurnal record
    :param record:
    :return: nothing, all results is a side effect in 'results' variable
    """
    for fingerprint in record['fingerprints']:
        vote = json.loads(base64.b64decode(fingerprint['metadata']))
        for answer in vote['answers']:
            question_title = answer['question']['title']
            question_result = results.get(question_title,None)
            if (question_result == None): question_result = {}; results[question_title]=question_result;
            for key, answer in answer['vote'].items():
                question_result[key]=question_result.get(key,0)+answer


class VotesPCounter:
    def __init__(self):
        pass

    def count(self, journalString):
        # Implement voting calc map-reduce task here
        # May be should use Pool.map for this

        votes = list()
        results = {}

        journal = json.loads(journalString);
        del journalString



        # parallel processing

        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:
            cpus = 2   # arbitrary default

        def iterator():
            return journal['records'].next(),results

        pool = multiprocessing.Pool(processes=cpus)
        pool.map(process_record, iterator())

        print(json.dumps(results, sort_keys=True, encoding="UTF-8", indent=4, separators=(',',': ')))

        return results


