from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Customer(models.Model):
    """
        Model that represents a FixIt Customer
        This is not a good example to use as reference for future models
        as this one has a relationship with django user        
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    city = models.CharField(max_length = 255)
    phone = models.CharField(blank = True, unique = True, max_length = 50)


    def __str__(self):
        return self.user.username

class UserChangePassword(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    chpwd_token = models.CharField(blank = True, null = True, max_length = 100, unique = True)

class TPagaCustomer(models.Model):
    """
        Model that saves de Tpago customer information
    """
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE, null = False)
    tpaga_id = models.CharField(max_length = 300, blank = False)
    token = models.CharField(max_length = 300, blank = True, null = True, unique = True)

class CreditCard(models.Model):
    credit_card_id = models.CharField(max_length = 300, blank = True, null = True, unique = True)
    card_holder_name = models.CharField(max_length = 300, blank = True, null = True)
    last_four = models.IntegerField()
    TYPE_CHOICES = ( ('VISA', 'VISA'), ('MASTERCARD', 'MASTERCARD'), ('AMEX', 'AMEX'), ('DINERS', 'DINERS') )
    type = models.CharField(max_length = 20, choices = TYPE_CHOICES, default = 'ORDERED')
    tpagaCustomer = models.ForeignKey(TPagaCustomer, on_delete=models.CASCADE)

    def __str__(self):
         return self.credit_card_id + " " + self.type + " " + str(self.last_four)

class Address(models.Model):
    """
        Model that represents an address of a customer       
    """
    name = models.CharField(max_length=255, help_text="short name to recognize the address")
    address = models.CharField(max_length=255, help_text="actual address")
    city = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255)
    customer = models.ForeignKey('Customer', related_name='addresses', on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.name + "  " + self.address


class Confirmation(models.Model):
    
     customer = models.ForeignKey('Customer', related_name='confirmations', on_delete=models.SET_NULL, null=True)
     expire_date = models.DateTimeField(auto_now = True, blank = True)
     code = models.CharField(max_length = 255)
     state = models.BooleanField(default = False)

     TYPE_CHOICES = (
        ('MAIL', 'MAIL'),
        ('SMS', 'SMS')
     )
     confirmation_type = models.CharField(max_length = 40, choices = TYPE_CHOICES, default = 'ORDERED')

     def __str__(self):
         return self.code



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
        receiver that creates a token for every user
    """
    if created:
        Token.objects.create(user=instance)
