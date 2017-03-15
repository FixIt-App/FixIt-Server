from django.db import models

class WorkType(models.Model):

     name = models.CharField(max_length = 255)
     description = models.CharField(max_length = 500)
     icon = models.CharField(max_length = 700)

     def __str__(self):
         return self.name