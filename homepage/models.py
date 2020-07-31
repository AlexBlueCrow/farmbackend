from django.db import models
from farmbackend.settings import MEDIA_ROOT
from dataserver.models import FarmUser
from zxserver.models import ZxItem
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
    name = models.CharField(max_length = 50 , default = '',blank = True)
    description = models.CharField(max_length = 50 , default = '')
    itemname = models.CharField(max_length = 50,default = '',unique = False, blank = True )
    farmname = models.CharField(max_length = 50,default = '',unique = False )
    video = models.FileField(upload_to = 'statics/video/',unique = True )
    def __str__(self):
        return self.farmname+self.itemname


class PicFiles(models.Model):
    itemname = models.CharField(max_length = 50,default = '',unique = False,blank = True)
    farmname = models.CharField(max_length = 50,default = '',unique = False )
    pic = models.FileField(upload_to = 'statics/video/', unique = True )

    def __str__(self):
        return self.farmname+self.itemname

class VIMap(models.Model):
    name = models.CharField(max_length = 50,default='')
    farm = models.ForeignKey(FarmUser, on_delete = models.CASCADE)
    item_id = models.IntegerField(blank=False,default=-1)
    video_id = models.IntegerField(blank=False,default=-1)

    def __str__(self):
        return self.name





        
