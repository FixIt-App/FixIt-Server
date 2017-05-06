from django.db import models
from worktype.models import WorkType
from customer.models import Customer, Address
from worker.models import Worker


class Work(models.Model):
    worktype = models.ForeignKey('worktype.WorkType', on_delete = models.CASCADE)
    customer = models.ForeignKey('customer.Customer', on_delete = models.CASCADE)
    address = models.ForeignKey('customer.Address', on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now = False, blank = False)
    description = models.TextField(blank = True)
    worker = models.ForeignKey('worker.Worker', on_delete = models.CASCADE, blank = True, null = True)
    asap = models.BooleanField(default = True)

    STATE_CHOICES = (
        ('ORDERED', 'ORDERED'),
        ('SCHEDULED', 'SCHEDULED'),
        ('FINISHED', 'FINISHED'),
        ('FAILED', 'FAILED'),
        ('CANCELED', 'CANCELED'),
        ('IN_PROGRESS', 'IN PROGRESS')
    )

    state = models.CharField(max_length = 20, choices = STATE_CHOICES, default = 'ORDERED')

    def __str__(self):
        return "Usuario: %s | Trabajo: %s | Hora: %s | Dirección: %s " % (self.customer.user.email, self.worktype.name, str(self.time), self.address.address, )
        
class DynamicPricing(models.Model):

    start = models.TimeField(auto_now = False, blank = False)
    end = models.TimeField(auto_now = False, blank = False)
    multiplier = models.DecimalField(max_digits=12, decimal_places=2, default = 1.0)

    def __str__(self):
        return str(self.start) + " - " + str(self.end)