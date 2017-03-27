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
    user = models.OneToOneField(User)
    city = models.CharField(max_length = 255)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
        receiver that creates a token for every user
    """
    if created:
        Token.objects.create(user=instance)


class Address(models.Model):
    """
        Model that represents an address of a customer       
    """
    name = models.CharField(max_length=255, help_text="short name to recognize the address")
    address = models.CharField(max_length=255, help_text="actual address")
    city = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255)
    customer = models.ForeignKey('Customer', related_name='addresses', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name + "  " + self.address

