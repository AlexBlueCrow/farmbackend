from django.db import models
from farmbackend.settings import MEDIA_ROOT
from dataserver.models import FarmUser
from django.contrib.auth.models import AbstractUser
# Create your models here.

class AdminUser(AbstractUser):
    phonenumber = models.BigIntegerField(blank=True,default=0,unique=True)
    farm = models.CharField(max_length=30,default='',blank=True)
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=20,default='farmuser')
    active = models.BooleanField(default=False)
    def __str__(self):
      return self.username

class StaticFiles(models.Model):
    
    identifier = models.CharField(max_length = 30,default='',unique=True)
    pic = models.FileField(upload_to='statics/pic/',unique= True)
    video =models.FileField(upload_to='statics/video/',unique=True)

    def __str__(self):
        return self.identifier

class VideoFiles(models.Model):
    itemname = models.CharField(max_length = 50,default='',unique=False)
    farmname = models.CharField(max_length = 50,default='',unique=False)
    video =models.FileField(upload_to='statics/video/',unique=True)
    
    

    def __str__(self):
        return self.farmname+self.itemname

class PicFiles(models.Model):
    itemname = models.CharField(max_length = 50,default='',unique=False)
    farmname = models.CharField(max_length = 50,default='',unique=False)
    pic =models.FileField(upload_to='statics/video/',unique=True)

    def __str__(self):
        return self.farmname+self.itemname




        
