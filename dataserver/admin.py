from django.contrib import admin
from .models import WxUser,FarmUser,Item,Order,Region,Question,Comments,Certification,Video,Prepay_Order,Varify_failed,MchInfo
# Register your models here.

admin.site.register([WxUser,FarmUser,Item,Order,Region,Question,Comments,Certification,Video,Prepay_Order,Varify_failed,MchInfo])

