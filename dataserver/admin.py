from django.contrib import admin
from .models import WxUser,FarmUser,Item,Order,Region,Question,Comments,Certification
# Register your models here.

admin.site.register([WxUser,FarmUser,Item,Order,Region,Question,Comments,Certification,Video])

