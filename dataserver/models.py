from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.


class WxUser(models.Model):
    user_openid = models.CharField(max_length =50,blank = False,default='',unique=True)
    user_gender = models.CharField(max_length=10,choices=[('female','female'),('male','male'),('null','null')],default = 'null')
    user_avatar = models.CharField(max_length=50,blank=True,default='')##头像地址
    user_nickname = models.CharField(max_length = 50,blank = False, default= '')
    user_address = models.CharField(max_length=100,blank=True,default='')
    user_phonenumber= models.BigIntegerField(blank=True,default=0) 
    user_addressee = models.CharField(max_length = 50,blank = False, default= '')
    user_membership = models.IntegerField(default=0)
    user_region = models.CharField(max_length=50,default='')

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
    farm_type = models.CharField(max_length = 20,default='')
    farm_rank = models.IntegerField(default=0)
    short = models.CharField(max_length=20,default='',blank=True)
    longitude = models.DecimalField(max_digits=8,decimal_places=4,default=0)
    latitude = models.DecimalField(max_digits=8,decimal_places=4,default=0)

    def __str__(self):
        return self.farm_name



class Item(models.Model):
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
    item_guaranteed = models.FloatField(default=0)
    item_benefit = models.CharField(max_length=200)
    item_period = models.IntegerField(blank=True,default=1)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name+'--'+str(self.item_price)

class Region(models.Model):

    region_name = models.CharField(max_length = 50,primary_key=True)
    farm = models.ForeignKey(FarmUser,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    region_address = models.CharField(max_length = 100)
    num_rows = models.IntegerField()
    num_lines = models.IntegerField()
    status = models.CharField(max_length = 500,default = 0)


    def __str__(self):
        return self.region_name+str（self.item）

class Certification(models.Model):
    farm = models.ForeignKey(FarmUser,on_delete=models.CASCADE)
    cer_type = models.CharField(max_length = 50)
    cer_name = models.CharField(max_length = 50)
    cer_pic_address = models.CharField(max_length = 50)
    cer_discription = models.CharField(max_length = 50,default='')

    def __str__(self):
        return self.farm


class Order(models.Model):
    num = models.CharField(primary_key=True,unique=True,max_length=25)
    item = models.ForeignKey(Item,on_delete=models.PROTECT)
    farm_name = models.CharField(max_length=30,default='',blank=True)
    wxuser = models.ForeignKey(WxUser,on_delete=models.PROTECT,default='')
    deliver_address = models.CharField(max_length = 50,default='',blank=False)
    effect_time = models.DateTimeField(default=timezone.now)
    timespanse = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    price_paid = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    quantity = models.IntegerField(default=1)
    price_origin = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    tree_ip = models.CharField(max_length=50,default = '')
    buyernickname = models.CharField(max_length=20,default='')
    benefit = models.CharField(max_length=50,default='')
    delivered = models.FloatField(default=0)
    guaranteed = models.FloatField(default=0)
    postsign = models.CharField(default='',max_length=50)
    imageUrl = models.CharField(default='',max_length=50)
    message_from_farm = models.CharField(default='',max_length=80,blank = True)
    phone_num = models.CharField(max_length = 30,default='')
    name_rec = models.CharField(max_length =20,default = '', blank = True )
    ip_line = models.IntegerField(default=0)
    ip_row =models.IntegerField(default=0)
    

    def __str__(self):
        return self.buyernickname+'--'+self.tree_ip+'--'+str(self.price_paid)
    
    def output(self):
        for item in self:
            print(item,self.item)
        return 
        

class Prepay_Order(models.Model):
    out_trade_no = models.CharField(primary_key=True, unique=True,max_length=20)
    sign = models.CharField(max_length=50)
    noncestr=models.CharField(max_length=50)
    openid=models.CharField(max_length=40)
    fee = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    item_id=models.IntegerField(blank=False)
    deliver_address = models.CharField(max_length = 50,default='',blank=False)
    quantity = models.IntegerField(default=1)
    buyernickname = models.CharField(max_length=20,default='')
    postsign = models.CharField(default='',max_length=50)
    varified = models.BooleanField(default=False)
    phone_num = models.CharField(max_length = 30,default='')
    name_rec = models.CharField(max_length =20,default = '', blank = True )
    

    def __str__(self):

        return self.buyernickname+'--'+str(self.fee)+str(self.varified)


class Varify_failed(models.Model):
    out_trade_no = models.CharField(primary_key=True, unique=True,max_length=20)
    sign = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    
    def __str__(self):
        return self.out_trade_no+'--'+str(self.fee)

class Question(models.Model):  
    Q_CHOICES = [('A','A'),('B','B'),('C','C'),('D','D')]
    question_id = models.IntegerField(primary_key=True,unique=True)
    question_category = models.CharField(max_length=20,default="无") 
    question_rank = models.IntegerField(default='1')  
    question_text = models.CharField(max_length = 50)
    question_reward = models.FloatField(default='0')
    option_A = models.CharField(max_length =20)
    option_B = models.CharField(max_length =20)
    option_C = models.CharField(max_length =20)
    option_D = models.CharField(max_length =20)
    
    correct_answer = models.CharField(max_length=1,choices = Q_CHOICES, default = '')

    def __str__(self):
        return str(self.question_id)+'--'+self.question_category+'--'+self.question_text

class Comments(models.Model):
    comment_id = models.AutoField(primary_key = True)
    item_id = models.IntegerField(default=0)
    comment_text = models.CharField(max_length = 100)
    wxuser = models.ForeignKey(WxUser,on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default= timezone.now)
    def __str__(self):
        return self.comment_text

class Video(models.Model):
    ##video_id
    video_address = models.CharField(max_length = 80)
    video_class = models.CharField(max_length = 20,default='')
    video_description =  models.CharField(max_length = 50)


class CollectiveOrder(models.Model):
    code = models.CharField(max_length = 30,unique=True,primary_key=True)
    companyname = models.CharField(max_length=20)
    contact = models.CharField(max_length = 20)
    phone_num = models.CharField(max_length=25,blank=True)
    wxid = models.CharField(max_length=20,blank=True)
    time = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(default=0.00,max_digits=8,decimal_places=2)

class GiftCode(models.Model):
    code = models.CharField(max_length = 30 ,unique=True,primary_key=True)
    item_id = models.IntegerField()
    is_used = models.BooleanField(default=False)
    tree_ip = models.CharField(max_length=20)
    owner = models.ForeignKey(CollectiveOrder,on_delete=models.CASCADE)
    ip_line = models.IntegerField(default=0)
    ip_row =models.IntegerField(default=0)

class MchInfo(models.Model):
    mch_id = models.CharField(max_length = 20)
    mch_key = models.CharField(max_length = 50)
    appid = models.CharField(max_length = 20)
    secret = models.CharField(max_length = 50)
    
    


    
















