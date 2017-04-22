from BaseNotification import BaseNotification

class WorkerAssignedNotification(BaseNotification):

    def __init__(work, priority = 10):
        BaseNotification.__init__(self, priority = priority)
        self.work = work


