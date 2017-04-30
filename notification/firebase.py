import json
import requests
import os

from notification.models import Notification

class Firebase(object):

    @staticmethod
    def send_notification(notification):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "key=%s" % os.environ.get('FIREBASE_CUSTOMER_KEY') 
        }
        r = requests.post('https://fcm.googleapis.com/fcm/send', data = json.dumps(notification.export()), headers = headers)
        if r.status_code >= 200 and r.status_code <= 300:
            return True
        else:
            return False
            
