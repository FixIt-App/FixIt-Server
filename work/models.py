from django.db import models
from worktype.models import WorkType
from customer.models import Customer, Address


class Work(models.Model):
    worktype = models.ForeignKey('worktype.WorkType', on_delete = models.CASCADE)
    customer = models.ForeignKey('customer.Customer', on_delete = models.CASCADE)
    address = models.ForeignKey('customer.Address', on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now = False, blank = False)
    description = models.TextField(blank = True)

    def __str__(self):
        return "Usuario: %s | Trabajo: %s | Hora: %s | Dirección: %s " % (self.customer.user.email, self.worktype.name, str(self.time), self.address.address, )
        
        