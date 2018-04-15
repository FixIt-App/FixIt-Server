

class BaseNotification():

    def __init__(self, data = {}, token = None, priority = 10, notification_type = None):
        self.priority = priority
        self.token = token
        self.data = data
        self.data['notification_type'] = notification_type
        self.data['icon'] = "fixit_push_image"
        self.data['color'] = "#12A19B"

    def export(self):
        # TODO: fabi mandar todo lo de data
         return {
            "message": {
                "token": self.token,
                "data": {
                    "icon": "aca deberia ir todo lo de self.data",
                },
                "notification": {
                    "body": self.data['message'],
                    "title": self.data['title']
                }
             }
         }

