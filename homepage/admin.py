from django.contrib  import admin
from .models import StaticFiles,AdminUser,VideoFiles,PicFiles,VIMap
# Register your models here.

admin.site.register([StaticFiles,AdminUser,VideoFiles,PicFiles,VIMap])
