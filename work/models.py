from django.db import models
from worktype.models import WorkType
from customer.models import Customer, Address
from worker.models import Worker
from customer.models import CreditCard
from django.contrib.postgres.fields import JSONField

class Rating(models.Model):
    score = models.IntegerField(blank = False)
    comment = models.TextField(blank = True, null = True)

    def __str__(self):
        return str(self.score)

class Work(models.Model):
    worktype = models.ForeignKey('worktype.WorkType', on_delete = models.CASCADE)
    customer = models.ForeignKey('customer.Customer', on_delete = models.CASCADE)
    address = models.ForeignKey('customer.Address', on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now = False, blank = False)
    description = models.TextField(blank = True)
    worker = models.ForeignKey('worker.Worker', on_delete = models.CASCADE, blank = True, null = True)
    asap = models.BooleanField(default = True)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, blank = True, null = True)

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
        return "Id %s  Usuario: %s - %s | Trabajo: %s | Hora: %s | Dirección: %s " % (str(self.id), self.customer.user.username, self.customer.user.id, self.worktype.name, str(self.time), self.address.address, )

class Transaction(models.Model):
    timestamp = models.TimeField(auto_now = True, blank = False)
    work = models.OneToOneField(Work, on_delete = models.CASCADE, blank = True, null = True)
    receipt_number = models.IntegerField(blank = False, unique = True, null = False)
    value = models.IntegerField(blank = False, null = False)
    credit_card = models.ForeignKey(CreditCard, on_delete = models.CASCADE, blank = True, null = True)
    STATE_CHOICES = (
        ('CREATING', 'CREATING'),
        ('CHARGE', 'CHARGE'),
        ('ROLLBACKED', 'ROLLBACKED'),
        ('PAYED', 'PAYED'),
    )
    state =  models.CharField(max_length = 20, choices = STATE_CHOICES, default = 'CREATING')
    third_party_response = JSONField(null = True, default = None, blank = True)

    def __str__(self):
        return str(self.receipt_number)

class TransactionItem(models.Model):
    trx = models.ForeignKey(Transaction, blank = False, null = False)
    description = models.TextField(blank = False, null = False)
    price = models.IntegerField(blank = False, null = False)
    TYPE_CHOICES = (
        ('SERVICE', 'SERVICE'),
        ('IVA', 'IVA'),
        ('SUBTOTAL', 'SUBTOTAL'),
        ('SUPPLY', 'SUPPLY'),
        ('TOTAL', 'TOTAL'),
    )
    item_type =  models.CharField(max_length = 20, choices = TYPE_CHOICES, default = 'SERVICE')
    bill_support = models.FileField(upload_to='uploads/%Y/%m/%d/', null = True, blank = True)


    def __str__(self):
        return str(self.id)


class DynamicPricing(models.Model):

    start = models.TimeField(auto_now = False, blank = False)
    end = models.TimeField(auto_now = False, blank = False)
    multiplier = models.DecimalField(max_digits=12, decimal_places=2, default = 1.0)

    def __str__(self):
        return str(self.start) + " - " + str(self.end)