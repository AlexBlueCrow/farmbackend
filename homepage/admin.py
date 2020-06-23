from django.contrib  import admin
from .models import StaticFiles,AdminUser
# Register your models here.

admin.site.register([StaticFiles,AdminUser])
