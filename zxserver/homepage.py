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
from zxserver.models import ZxUser,ZxItem,ZxOrder,ZxComments,ZxPrepay_Order,ZxVarify_failed,Captain,CapManager
from dataserver.models import FarmUser
from dataserver.serializers import FarmUserSerializer
from zxserver.serializers import ZxUserSerializer,ZxItemSerializer,ZxOrderSerializer,ZxCommentsSerializer,ZxPrepay_OrderSerializer,CaptainSerializer
import random
from dataserver.login import wx_login
import time
import datetime
import xml.etree.ElementTree as ET
from zxserver import pay
from rest_framework.decorators import api_view,authentication_classes
from wechatpy.utils import check_signature
from wechatpy.pay.api import WeChatOrder
from wechatpy.pay import WeChatPay
from pprint import pprint
from json import dumps 
import operator
from math import radians, cos, sin, asin, sqrt
import random,string
from django.core.serializers.json import json
import csv


def homepage(request):
    
    return render(request,'homepage.html')