from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from dataserver import views



urlpatterns = [
    url(r'getItem/(?P<pk>\d+)$',views.get_item),
    url(r'login',views.login),
    
]