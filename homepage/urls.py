from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.views.static import serve
from farmbackend.settings  import MEDIA_ROOT
from . import login
urlpatterns = [
    url(r'order_inquire/$',views.order),
    url(r'ZxItem/$',views.ZxItem_API),
    url(r'csrf_token/',views.get_csrf_token),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),
    url(r'login/$',login.login),
    url(r'register',login.register),
    url(r'csv/',views.csv),
    url(r'getUserInfo/',login.userInfo),
    url(r'itemList/',views.ZxItem_API),
    url(r'farm/',views.Farm_API),
    url(r'ZxItem_update',views.ZxItem_update),
    url(r'video/',views.video_API),
    url(r'VIMap/',views.VIMap_update)
]

