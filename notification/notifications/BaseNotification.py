

class BaseNotification():

    def __init__(self, notification = {}, to = None, priority = 10, notification_type = None):
        self.priority = priority
        self.to = to
        self.notification = notification
        self.notification['notification_type'] = notification_type
        self.notification['icon'] 

    def export(self):
         return {
            "priority": self.priority,
            "to":    self.to,
            "data": self.notification,
         }

