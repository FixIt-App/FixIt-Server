import json
import requests
import os
from oauth2client.service_account import ServiceAccountCredentials
from notification.models import Notification

class Firebase(object):

    URL = "https://fcm.googleapis.com/v1/projects/fixit-463da/messages:send"  
    FCM_SCOPE = ['https://www.googleapis.com/auth/firebase.messaging']

    @staticmethod
    def get_access_token():
        service_account = os.environ['FCM_SERVICE_ACCOUNT_PATH']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account, Firebase.FCM_SCOPE)
        access_token_info = credentials.get_access_token()
        return access_token_info.access_token

    @staticmethod
    def send_notification(notification):
        headers = {
            'Authorization': 'Bearer ' + Firebase.get_access_token(),
            'Content-Type': 'application/json; UTF-8',
        }
        
        r = requests.post(Firebase.URL, data = json.dumps(notification.export()), headers = headers)
        if r.status_code >= 200 and r.status_code <= 300:
            return True
        else:
            return False
            
