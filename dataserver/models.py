from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
# Create your models here.


class WxUser(models.Model):
    user_openid = models.CharField(max_length =50,blank = False,default='',unique=True)
    user_address = models.CharField(max_length=100,blank=True,default='')
    user_phonenumber= models.BigIntegerField(blank=True,default=0)
    user_nickname = models.CharField(max_length = 50,blank = False, default= '')
    user_addressee = models.CharField(max_length = 50,blank = False, default= '')

    def __str__(self):
        return self.user_openid


class FarmUser(models.Model):
    #farm_id = models.AutoField()
    farm_name = models.CharField(max_length = 50,unique=True)
    farm_address = models.CharField(max_length = 100)
    farm_description = models.CharField(max_length = 300)
    farm_logo_address = models.CharField(max_length = 100)
    farm_phonenumber = models.BigIntegerField(blank=True,default=0)
    farm_contact = models.CharField(max_length = 20)

    def __str__(self):
        return self.farm_name



class Item(models.Model):
    #item_id = models.AutoField()
    item_name = models.CharField(max_length = 100,blank=False,default='')
    owner = models.ForeignKey(FarmUser,on_delete=models.PROTECT)
    category = models.CharField(max_length= 100,blank=False,default='')
    vedio_address = models.CharField(max_length=400)##vedio url
    pic_address = models.CharField(max_length=400)##pic url
    item_description = models.CharField(max_length=600,blank=True)
    item_price = models.IntegerField()
    item_num_available = models.IntegerField()
    item_guarantee = models.IntegerField()
    item_benefit = models.CharField(max_length=200)
    item_period = models.IntegerField(blank=True,default=1)

    def __str__(self):
        return self.item_name

class Region(models.Model):
    #region_id = models.AutoField()
    region_name = models.CharField(max_length = 50)
    farm = models.ForeignKey(FarmUser,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    region_address = models.CharField(max_length = 100)
    num_rows = models.IntegerField()
    num_lines = models.IntegerField()

    def __str__(self):
        return self.region_name

class Certification(models.Model):
    farm = models.ForeignKey(FarmUser,on_delete=models.CASCADE)
    cer_type = models.CharField(max_length = 50)
    cer_name = models.CharField(max_length = 50)
    cer_pic_address = models.CharField(max_length = 50)

    def __str__(self):
        return self.farm


class Order(models.Model):
    order_num = models.IntegerField(primary_key=True,unique=True)
    order_wxuser = models.ForeignKey(WxUser,on_delete=models.PROTECT,default='')
    order_deliver_address = models.CharField(max_length = 50,default='',blank=False)
    order_item = models.ForeignKey(Item,on_delete=models.PROTECT)
    order_effect_time = models.DateTimeField(default=timezone.now)
    order_is_active = models.BooleanField(default=True)
    order_price_paid = models.IntegerField()
    order_quantity = models.IntegerField()
    order_price_origin = models.IntegerField()
    order_tree_ip = models.CharField(max_length=50)

class Question(models.Model):
    Q_CHOICES = [('A','A'),('B','B'),('C','C'),('D','D')]
    question_id = models.AutoField(primary_key = True)
    question_text = models.CharField(max_length = 50)
    option_A = models.CharField(max_length =10)
    option_B = models.CharField(max_length =10)
    option_C = models.CharField(max_length =10)
    option_D = models.CharField(max_length =10)
    Answer = models.CharField(max_length=1,choices = Q_CHOICES, default = 'A')

class Comments(models.Model):
    comment_id = models.AutoField(primary_key = True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    comment_text = models.CharField(max_length = 100)
    wxuser = models.ForeignKey(WxUser,on_delete=models.CASCADE)























