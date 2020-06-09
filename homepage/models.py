from django.db import models
from farmbackend.settings import MEDIA_ROOT
# Create your models here.
class AdminUser(models.Model):
    userId = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length = 80)

class StaticFiles(models.Model):
    item_name = models.CharField(max_length = 30 )
    pic = models.FileField(upload_to='statics/pic/',unique= True)
    video =models.FileField(upload_to='statics/video/',unique=True)

