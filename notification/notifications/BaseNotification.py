import jsonpickle

class BaseNotification():

    def __init__(priority = 10):
        self.priority = priority
        
    def export(self):
         return jsonpickle.encode(self)

