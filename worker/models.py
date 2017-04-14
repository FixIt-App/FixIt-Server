from django.db import models

from django.contrib.auth.models import User
from worktype.models import WorkType

class Worker(models.Model):

    user = models.OneToOneField(User)
    phone = models.CharField(blank = True, unique = True, max_length = 50)
    document_id = models.CharField(blank = True, unique = True, max_length = 50)
    rh = models.CharField(blank = True, max_length = 10)
    profile_pic = models.ImageField(null=True, upload_to='workers/')
    works = models.ManyToManyField(WorkType)
    
