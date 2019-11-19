from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from dataserver import views
from dataserver import login




urlpatterns = [
    url(r'getItem/$',views.get_item),
    url(r'getQuestions/$',views.get_questions),
    url(r'login',login.wx_login),
    url(r'payOrder/res/',views.pay_res),
    url(r'payOrder/$',views.payOrder),
    
]