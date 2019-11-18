
import hashlib
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from dataserver.models import WxUser,Item,FarmUser,Question,Order
from dataserver.serializers import WxUserSerializer,ItemSerializer,OrderSerializer,FarmUserSerializer,QuestionSerializer
from login import wx_login
import random
import time
import datetime
import xml.etree.ElementTree as ET
from . import pay


# Create your views here.
mch_id=1560463491

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs) 

def get_farmuser(request):
    farmuser = FarmUser.objects.all()
    farmuser_serializer = FarmUserSerializer(farmuser,many=True)
    return JSONResponse(farmuser_serializer.data)

def get_item(request):
    pk=request.GET.get('pk')
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        pk=1
        item = Item.objects.get(id=pk)
    print(item)
    item_serializer = ItemSerializer(item,many=False)
    print(item_serializer.data)
    return JSONResponse(item_serializer.data)

def get_questions(request):
    category=request.GET.get('cate')
    print("cate:",category)
    try:
        questions = Question.objects.filter(question_category=category)
        print(questions)
    except Question.DoesNotExist:

        return HttpResponseNotFound
    
    questions_serializer = QuestionSerializer(questions,many=True)
    return JSONResponse(questions_serializer.data)




def payOrder(request):
    import time
    if request.method == 'POST':
        #获取价格
        
        price = (request.POST.get("item_price")*request.POST.get("buy_num")-request.POST.get("reward"))
 
        #获取客户端ip
        client_ip,port=request.get_host().split(":")
 
        #获取小程序openid
        JSCODE = request.POST.get('code')
        appid= 'wx48c0b0d820c4563d'
        secret='4acdae8837a2d8e8a6a675193394eed1'
        wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
        res = json.loads(requests.get(wxLoginURL).content)
        if 'errcode' in res:
            return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
        openid=res['openid']


 
        #请求微信的url
        url= 'https://api.mch.weixin.qq.com/pay/unifiedorder'
 
        #拿到封装好的xml数据
        body_data=pay.get_bodyData(openid,client_ip,price)
 
        #获取时间戳
        timeStamp=str(int(time.time()))
 
        #请求微信接口下单
        respone=requests.post(url,body_data.encode("utf-8"),headers={'Content-Type': 'application/xml'})
 
        #回复数据为xml,将其转为字典
        content=pay.xml_to_dict(respone.content)
        print(content)
 
        if content["return_code"]=='SUCCESS':
            #获取预支付交易会话标识
            prepay_id =content.get("prepay_id")
            #获取随机字符串
            nonceStr =content.get("nonce_str")
 
            #获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign=pay.get_paysign(prepay_id,timeStamp,nonceStr)
 
            #封装返回给前端的数据
            data={"prepay_id":prepay_id,"nonceStr":nonceStr,"paySign":paySign,"timeStamp":timeStamp}
 
            return HttpResponse(packaging_list(data))
 
        else:
            return HttpResponse("请求支付失败")

#def get_questions():

#def get_farmuser():

#def data_response():

#def get_wxuser(request):
    
