from django.db import models

class Image(models.Model):

     work =  models.ForeignKey('work.work', on_delete=models.CASCADE, null=True)
     image = models.ImageField(null=False)

     def __str__(self):
         return "ID: %s | ID Work: %s | Hora: %s | Dirección: %s " % (self.id,self.id_work)