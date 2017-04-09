from django.db import models

class Image(models.Model):

     work =  models.ForeignKey('work.work', on_delete=models.CASCADE, null=True)
     image = models.ImageField(null=False)

     def __str__(self):
         return "ID: %s" % (self.id)