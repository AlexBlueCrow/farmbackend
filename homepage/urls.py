from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.views.static import serve
from farmbackend.settings  import MEDIA_ROOT
urlpatterns = [
    url(r'order_inquire/$',views.order),
    url(r'ZxItem/$',views.ZxItem_API),
    url(r'csrf_token/',views.get_csrf_token),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),
]

