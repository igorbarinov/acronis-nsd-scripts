#!/usr/bin/env python
# Author: Igor Barinov <igorbarinov@me.com>

import cPickle as pickle
from Crypto.PublicKey import RSA
from Crypto import Random
import Crypto.Util.number as CUN
import os


# setup loggging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# and progressbar
from tqdm import *

random_generator = Random.new().read
"""

This script generates private/public keys for number of users defined in
NUMBER_OF_VOTERS constant.

"""

NUMBER_OF_VOTERS = 100000;

def create_keys(voters):
    publicpair ={}
    privatepair ={}
    logger.info("Starting generation of keys")
    for i in tqdm(range(1,voters+1)):
        key = RSA.generate(1024, random_generator)
        publickey = key.publickey().exportKey(format='PEM')
        privatekey = key.exportKey(format='PEM')
        publicpair[i] = publickey
        privatepair[i] = privatekey

    # dump to pickle file for later usage
    pickle.dump(publicpair, open("data/public_keys.p", "wb"))
    pickle.dump(privatepair, open("data/private_keys.p", "wb"))
    logger.info("Finished generation of keys. Check data/ folder.")

if __name__ == '__main__':
    create_keys(NUMBER_OF_VOTERS)
