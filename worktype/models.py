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
     price = models.IntegerField(default = -1)
     order = models.IntegerField(blank = True, null = True)
     url_name = models.CharField(max_length = 50, blank = True, null = True, unique = True)

     class Meta:
         verbose_name = "WorkType"
         verbose_name_plural = "WorkTypes"
         ordering = ['-order',]


     def __str__(self):
         return self.name

class Category(models.Model):
    name = models.CharField(max_length = 255)
    worktypes = models.ManyToManyField(WorkType)
    order = models.IntegerField(blank = True, null = True)


    class Meta:
         verbose_name = "WorkTypeCategory"
         verbose_name_plural = "WorkTypeCategories"
         ordering = ['order',]

    def __str__(self):
        return self.name
