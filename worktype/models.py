from django.db import models

class WorkType(models.Model):

     name = models.CharField(max_length = 255)
     description = models.CharField(max_length = 500)
     icon = models.ImageField(null = False)

     def __str__(self):
         return self.name

class Category(models.Model):
    name = models.CharField(max_length = 255)
    worktypes = models.ManyToManyField(WorkType)

    def __str__(self):
        return self.name
