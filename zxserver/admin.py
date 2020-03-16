from django.contrib import admin
from .models import ZxUser,ZxItem,ZxOrder,ZxComments,ZxPrepay_Order,ZxVarify_failed,Captain
# Register your models here.

admin.site.register([ZxUser,ZxItem,ZxOrder,ZxComments,ZxPrepay_Order,ZxVarify_failed,Captain])

