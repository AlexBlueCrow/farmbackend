from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from dataserver.models import FarmUser

# Create your models here.


class ZxUser(models.Model):
    user_openid = models.CharField(max_length =50,blank = False,default='',unique=True)
    user_gender = models.CharField(max_length=10,choices=[('female','female'),('male','male'),('null','null')],default = 'null')
    user_avatar = models.CharField(max_length=150,blank=True,default='')##头像地址
    user_nickname = models.CharField(max_length = 50,blank = False, default= '')
    user_address = models.CharField(max_length=100,blank=True,default='')
    user_phonenumber= models.BigIntegerField(blank=True,default=0) 
    user_addressee = models.CharField(max_length = 50,blank = False, default= '')
    user_membership = models.IntegerField(default=0)
    user_region = models.CharField(max_length=50,default='')
    current_captain_id = models.IntegerField(blank=True,default=-1)

    def __str__(self):
        return self.user_nickname

class ZxItem(models.Model):
    ##id ++
    
    item_name = models.CharField(max_length = 100,blank=False,default='')
    owner = models.ForeignKey(FarmUser,on_delete=models.PROTECT)
    category = models.CharField(max_length= 100,blank=False,default='')
    video_address = models.CharField(max_length=400)##video url
    pic_address = models.CharField(max_length=400)##pic url
    item_description = models.CharField(max_length=600,blank=True)
    item_price = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    item_num_total = models.IntegerField(default=0)
    item_num_sold = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    unit = models.CharField(max_length=5,default='',blank=False)
    def __str__(self):
        return self.item_name+'--'+str(self.item_price)+'/'+self.unit


class Captain(models.Model):
    captain_id = models.AutoField(primary_key=True)
    zxuser = models.ForeignKey(ZxUser,on_delete=models.PROTECT)
    longitude = models.DecimalField(max_digits=8,decimal_places=4,default=0)
    latitude = models.DecimalField(max_digits=8,decimal_places=4,default=0)
    addresss = models.CharField(max_length=40)
    phonenumber= models.BigIntegerField(blank=True,default=0)
    name = models.CharField(max_length =20,default = '', blank = True )
    active = models.BooleanField(default = False)

class ZxOrder(models.Model):
    num = models.CharField(primary_key=True,unique=True,max_length=25)
    item = models.ForeignKey(ZxItem,on_delete=models.PROTECT)
    farm_name = models.CharField(max_length=30,default='',blank=True)
    wxuser = models.ForeignKey(ZxUser,on_delete=models.PROTECT,default='')
    deliver_address = models.CharField(max_length = 50,default='',blank=False)
    effect_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    price_paid = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    quantity = models.IntegerField(default=1)
    price_origin = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    imageUrl = models.CharField(default='',max_length=50)
    phone_num = models.CharField(max_length = 30,default='')
    name_rec = models.CharField(max_length =20,default = '', blank = True )
    captain_id = models.IntegerField(blank=True,default=-1)
    deliver_time = models.CharField(max_length = 30,default = '')
    def __str__(self):
        return self.wxuser.user_nickname+'--'+str(self.price_paid)+'--'+self.item.item_name+'/'+str(self.captain_id)
        

class ZxPrepay_Order(models.Model):
    out_trade_no = models.CharField(primary_key=True, unique=True,max_length=20)
    sign = models.CharField(max_length=50)
    noncestr=models.CharField(max_length=50)
    openid=models.CharField(max_length=40)
    fee = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    item_id=models.IntegerField(blank=False)
    deliver_address = models.CharField(max_length = 50,default='',blank=False)
    quantity = models.IntegerField(default=1)
    varified = models.BooleanField(default=False)
    phone_num = models.CharField(max_length = 30,default='')
    name_rec = models.CharField(max_length =20,default = '', blank = True)
    captain_id = models.IntegerField(blank=True,default=-1)
    deliver_time = models.CharField(max_length = 30,default = '')
    def __str__(self):
        return str(self.fee)+str(self.varified)+self.out_trade_no


class ZxVarify_failed(models.Model):
    out_trade_no = models.CharField(primary_key=True, unique=True,max_length=20)
    sign = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    def __str__(self):
        return self.out_trade_no+'--'+str(self.fee)


class ZxComments(models.Model):
    comment_id = models.AutoField(primary_key = True)
    item_id = models.IntegerField(default=0)
    comment_text = models.CharField(max_length = 100)
    zxuser = models.ForeignKey(ZxUser,on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default= timezone.now)
    user_avatar = models.CharField(max_length=150,blank=True,default='')##头像地址
    user_nickname = models.CharField(max_length = 50,blank = False, default= '')
    def __str__(self):
        return self.user_nickname+'-'+self.comment_text




    
    


    
















