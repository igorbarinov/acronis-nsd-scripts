from locust import HttpLocust, TaskSet, task
import requests

AL_JOURNAL = "3daa3c16-2dff-4b4f-be66-360102d22a5e"
AL_HOST = "http://167.114.247.67:8080"
AL_HOST ="http://52.3.249.219:8080"

AL_AUTH = "Basic NGY3NGY4ODUtMDJlZi00ZDFlLWFmNjktYmU5NmFlOTY0MTI5OmV5SnJhV1FpT2lKclpYa2lMQ0poYkdjaU9pSlNVekkxTmlJc0ltRmpZMlZ6YzFSdmEyVnVTV1FpT2lJMFpqYzBaamc0TlMwd01tVm1MVFJrTVdVdFlXWTJPUzFpWlRrMllXVTVOalF4TWpraWZRLmV5SnpZMjl3WlhNaU9sc2lRVU5EUlZOVFgxUlBTMFZPSWwwc0ltcDBhU0k2SW14WVgwRnNUbVJyY2tsMk9ITnBSMDFCZGxOTWMzY2lMQ0pwWVhRaU9qRTBOVFF3TlRReU5qUXNJbWx6Y3lJNklrRmpjbTl1YVhNZ1RHVmtaMlZ5SW4wLk5keWQwQnFtczhDNUpWY25LQTNpN1ZsM1I4Vmh6bHpWY3NVRDF6OVVRTzNOazFsbURIWmxVTVpnTVU3eVFzd0czbUJWN1FRa2F1WWltZl9kczFOQWI2STZCTmlLcEQtZ2I1M2F1SHdUTUVUYl8tVmVqRGpUVWhSRlplaXlmcmd0dlpMQ0dDamo1cmpXazdidHM0WXRvVUVyRlBMT1p2UGRXMkFJMFBJaXdJZUZpa3dlWEd5T1NNMnQ5NFlubWVYbWV2OUYyaUUxTzZ1WDQxeHF2bXYwN3Q1b1JXaUVHZWZTM3ZpUzliNzN0b0puY1FLeExhcXVHekJqVElpQzZnMWVzWm9ZbUV2VFFDSnlhUlJneFY2bmZPVy1VdDJGMzhYSkQ2LXozLV9XVkN6Q1YzUTRFeWRqNjNGQlFVcmhVcDVtVGZDSUt4clNoXy1UOVBINHJrTW1tZw=="
class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.headers = {"Authorization":AL_AUTH,'Content-Type':'application/json'}
        self.s = requests.Session()
        self.s.headers.update({'Authorization': AL_AUTH, 'Content-Type':'application/json'})

    @task(1)
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
