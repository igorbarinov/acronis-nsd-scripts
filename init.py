import requests
from requests.auth import HTTPBasicAuth
from ConfigParser import SafeConfigParser
from faker import Factory
from base64 import b64encode
import sys, os

faker = Factory.create()

parser = SafeConfigParser()
parser.read('load.ini')
AL_HOST = parser.get('general', 'host')
headers = {'Content-Type':'application/json'}


def create_user():
    r = requests.post(AL_HOST + '/api/users', headers= headers, data =  '{"email": " ' + faker.email() + ' "}')
    key = str(r.json()["accessTokens"][0]["accessKey"])
    secret = str(r.json()["accessTokens"][0]["accessSecret"])
    userAndPass = "Basic " + b64encode(key + ":" + secret).decode("ascii")
    return userAndPass

AL_AUTH = str(create_user())
parser.set('general', 'auth', AL_AUTH)

def create_journal():
    payload = '{"name": "' + faker.name() + '", "type": "blockchain_merkletree"}'
    headers = {'Content-Type':'application/json', "Authorization":AL_AUTH }
    r = requests.post(AL_HOST + '/api/journals', headers = headers, data = payload)
    return r.json()["id"]

AL_JOURNAL = str(create_journal())
parser.set('general', 'journal', AL_JOURNAL)

with open('load.ini', 'w') as configfile:    # save
    parser.write(configfile)
