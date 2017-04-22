

class BaseNotification():

    def __init__(self, notification = {}, to = None, priority = 10):
        self.priority = priority
        self.to = to
        self.notification = notification
        
    def export(self):
         return {
            "priority": self.priority,
            "to": self.to,
            "notification": self.notification
         }

