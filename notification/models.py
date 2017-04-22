from django.db import models

from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField


class NotificationToken(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    token = models.TextField(blank = False, unique = True)
    TYPE_CHOICES = (
        ('WORKER', 'WORKER'),
        ('CUSTOMER', 'CUSTOMER'),
    )
    token_type = models.CharField(max_length = 20, choices = TYPE_CHOICES, null = True)

    PLATFORM_CHOICES = (
        ('ANDROID', 'Android'),
        ('IOS', 'IOS (Apple)'),
    )
    platform_type = models.CharField(max_length = 20, choices = PLATFORM_CHOICES, null = True)

    def __str__(self):
        return self.token

class Notification(models.Model):

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    payload = HStoreField(null = True, default = None)
    TYPE_CHOICES = (
        ('WC', 'WORK CREATED'),
        ('WA', 'WORKER ASSIGNED'),
        ('PR', 'PROMOTIONAL')
    )
    
    notification_type = models.CharField(max_length = 20, choices = TYPE_CHOICES)

    STATE_CHOICES = (
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed')
    )

    state = models.CharField(max_length = 20, choices = STATE_CHOICES, null = True)

    def __str__(self):
        return str(self.id)
        
