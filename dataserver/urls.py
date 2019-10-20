from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from dataserver import views



urlpatterns = [
    url(r'getItem/(?P<id>(\d+))$',views.get_item),
    url(r'getQuestion/(?P<item_id>(\d+))$',views.get_questions),
    url(r'login',views.login),
    
]