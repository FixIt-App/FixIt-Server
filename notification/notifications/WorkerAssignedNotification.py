from .BaseNotification import BaseNotification

class WorkerAssignedNotification(BaseNotification):

    def __init__(to = None, priority = 10):
        BaseNotification.__init__(self, priority = priority, to = to)
        self.notification = notification


