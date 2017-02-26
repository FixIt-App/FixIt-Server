from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Customer(models.Model):
    """
        Model that represents a FixIt Customer
    """
    user = models.OneToOneField(User)
    city = models.CharField(max_length = 255)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
        receiver that creates a token for every user
    """
    if created:
        Token.objects.create(user=instance)




