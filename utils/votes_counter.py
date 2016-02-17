#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Vladimir Buzov <vladimir.buzov@gmail.com>

import json
import base64

class VotesCounter:
    def __init__(self):
        pass

    def count(self, journalString):
        # Implement voting calc map-reduce task here
        # May be should use Pool.map for this

        votes = list()

        journal = json.loads(journalString);
        for record in journal['records']:
            for fingerprint in record['fingerprints']:
                votes.append(
                    json.loads(
                        base64.b64decode(fingerprint['metadata'])
                    )
                )

        results = {}

        for vote in votes:
            for answer in vote['answers']:
                question_title = answer['question']['title']
                question_result = results.get(question_title,None)
                if (question_result == None): question_result = {}; results[question_title]=question_result;
                for key, answer in answer['vote'].items():
                    question_result[key]=question_result.get(key,0)+answer


        print(json.dumps(results, sort_keys=True, indent=4, separators=(',',': ')))

        result = {'txid': '74dc7d0cadf60bbb1d06a99f41db7b0a4e620d4c66cdc020729796e6fd0b8260'}

        return result
