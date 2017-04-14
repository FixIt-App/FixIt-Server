from django.db import models

class WorkType(models.Model):

     name = models.CharField(max_length = 255)
     description = models.CharField(max_length = 500)
     icon = models.ImageField(null = False)

     TYPE_CHOICES = (
        ('STANDARIZED', 'STANDARIZED'),
        ('NOT_STANDARIZED', 'NOT_STANDARIZED'),
        ('UNKNOWN', 'UNKNOWN')
     )

     price_type = models.CharField(max_length = 40, choices = TYPE_CHOICES, default = 'ORDERED')
     price = models.DecimalField(max_digits=12, decimal_places=2, default = -1.0)

     def __str__(self):
         return self.name

class Category(models.Model):
    name = models.CharField(max_length = 255)
    worktypes = models.ManyToManyField(WorkType)

    def __str__(self):
        return self.name
