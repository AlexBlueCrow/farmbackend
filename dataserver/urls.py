from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from dataserver import views
from dataserver import login




urlpatterns = [
    url(r'getItem/$',views.get_item),
    url(r'getQuestions/$',views.get_questions),
    url(r'login',login.wx_login),
    url(r'login/update',login.wx_update),
    url(r'pay_feedback',views.pay_feedback),
    url(r'payOrder/$',views.payOrder),
    url(r'getComments/',views.get_comments),
    url(r'postComment/',views.post_comment),
    url(r'weChatPay/',views.weChatPay),  
    url(r'getFarmInfo/',views.get_farmInfo),
    url(r'getOrderInfo/',views.get_orderInfo) 
]