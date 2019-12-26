from rest_framework.response import Response
import hashlib
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from dataserver.models import WxUser,Item,FarmUser,Question,Order,Comments,Prepay_Order,Region
from dataserver.serializers import WxUserSerializer,ItemSerializer,OrderSerializer,FarmUserSerializer,QuestionSerializer,CommentsSerializer,Prepay_OrderSerializer,RegionSerializer
from dataserver.login import wx_login
import random
import time
import datetime
import xml.etree.ElementTree as ET
from dataserver import pay
from rest_framework.decorators import api_view,authentication_classes
from wechatpy.utils import check_signature
from wechatpy.pay.api import WeChatOrder
from wechatpy.pay import WeChatPay
from pprint import pprint
from json import dumps 

def order_manager(request):
    render(request,'qingjiao_manage.html')
