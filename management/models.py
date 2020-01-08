from django.db import models

# Create your models here.



class User (models.Model):
    name = models.CharField(max_length=40,unique = True )
    password = models.CharField(max_length=128)
    authority = models.CharField(max_length = 20)
    def __str__(self):
        return self.name

