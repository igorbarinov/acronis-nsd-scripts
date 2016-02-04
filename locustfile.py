from locust import HttpLocust, TaskSet, task
import requests
from ConfigParser import SafeConfigParser
import datetime

parser = SafeConfigParser()
parser.read('load.ini')
AL_JOURNAL = parser.get('general', 'journal')
AL_HOST = parser.get('general', 'host')
AL_AUTH = parser.get('general','auth')

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.headers = {"Authorization":AL_AUTH,'Content-Type':'application/json'}
        self.s = requests.Session()
        self.s.headers.update({'Authorization': AL_AUTH, 'Content-Type':'application/json'})

    #weight for task in ()
    # @task(1)
    # def timestamp(self):
    #     self.s.post(AL_HOST+'/api/journals/' + AL_JOURNAL +'/timestamp')
    #     print "timestamp journal " + str(datetime.datetime.now())

    @task(100)
    def create_record(self):
        r = self.client.post("/api/records", '{}')
        payload = '{"metadata":"eyJoYXNoIjogICIxMjMifQ==","metadataContentType":"application/json;enc=v1","metadataHash":"91af9b86a1afc344bda161d0255071f34a331a7a4bd929465cfd0eadd17129c0","nonce":"MTIzNDU2"}'
        # add fingerprint
        record_id = r.json()['id']
        self.s.post(AL_HOST + "/api/records/" + record_id + "/fingerprints", payload)
        # commit the record to a journal
        self.s.post(AL_HOST+'/api/journals/' + AL_JOURNAL + '/commit/' + record_id, '{}')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
