
from flatten_json import flatten

class BaseNotification():

    def __init__(self, data = {}, token = None, priority = 10, notification_type = None):
        self.priority = priority
        self.token = token
        self.data = data
        self.data['notification_type'] = notification_type
        self.data['icon'] = "fixit_push_image"
        self.data['color'] = "#12A19B"

    def dictToString(self, dict):
        for key, value in dict.items():
            if not isinstance(value, str):
                dict[key] = str(value)
        return dict

    def export(self):
        flat_data = flatten(self.data, separator = ".")
        flat_data_all_strings = self.dictToString(flat_data)
        return {
            "message": {
                "token": self.token,
                "data": flat_data_all_strings,
                "notification": {
                    "body": self.data['message'],
                    "title": self.data['title']
                }
            }
        }

