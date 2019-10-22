from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from dataserver import views
from dataserver import login



urlpatterns = [
    url(r'getItem/$',views.get_item),
    url(r'getQuestion/$',views.get_questions),
    url(r'login',login.wx_login),
    
]