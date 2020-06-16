from django.db import models
from farmbackend.settings import MEDIA_ROOT
from dataserver.models import FarmUser
# Create your models here.
class AdminUser(models.Model):
    userId = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length = 80)
    phonenumber = models.BigIntegerField(blank=True,default=0,unique=True)
    farm = models.ForeignKey(FarmUser,blank=True,on_delete=models.CASCADE)
    userName = models.CharField(max_length=15)
    role = models.CharField(max_length=20,default='farmuser')
     
    def __str__(self):
        return self.userId

class StaticFiles(models.Model):
    identifier = models.CharField(max_length = 30,default='',unique=True)
    pic = models.FileField(upload_to='statics/pic/',unique= True)
    video =models.FileField(upload_to='statics/video/',unique=True)

    def __str__(self):
        return self.identifier
        
