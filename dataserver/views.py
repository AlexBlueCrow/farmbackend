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
from dataserver.models import WxUser,Item,FarmUser,Question,Order,Comments
from dataserver.serializers import WxUserSerializer,ItemSerializer,OrderSerializer,FarmUserSerializer,QuestionSerializer,CommentsSerializer
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




# Create your views here.


 

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs) 

def get_farms(request):
    farmuser = FarmUser.objects.all()
    farmuser_serializer = FarmUserSerializer(farmuser,many=True)
    return JSONResponse(farmuser_serializer.data)

def get_item(request):
    items = Item.objects.all()
    items_serializer = ItemSerializer(items,many=True)
    return JSONResponse(items_serializer.data)

def get_orderInfo(request):
    code = request.GET.get('code')
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return HttpResponse(res[errorcode])
    openid=res['openid']
    wxuser = WxUser.objects.filter(user_openid=openid)
    orders = Order.objects.filter(order_wxuser=wxuser)
    print(orders)
    if orders:
        orders_serializer = OrderSerializer(orders,many=True)
        return JSONResponse(orders_serializer.data)
    else:
        return HttpResponse("无有效订单")


    

def get_farmInfo(request):
    id = request.GET.get('farm')
    farm =FarmUser.objects.filter(id=id)
    farm_serializer = FarmUserSerializer(farm,many=True)

    return JSONResponse(farm_serializer.data)

def get_questions(request):
    category=request.GET.get('cate')
    
    try:
        questions = Question.objects.filter(question_category=category)
    except Question.DoesNotExist:

        return HttpResponseNotFound
    
    questions_serializer = QuestionSerializer(questions,many=True)
    return JSONResponse(questions_serializer.data)


def get_comments(request):
    item_id = request.GET.get('item_id')
    comments = Comments.objects.filter(item_id=item_id)
    comments_serializer = CommentsSerializer(comments,many=True)
    
    return JSONResponse(comments_serializer.data)

@api_view(['GET'])
@authentication_classes([]) 
def post_comment(request):
    code = request.GET.get('code')
    comment_text = request.GET.get('comment')
    item_id = request.GET.get('item_id')
    
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
    openid=res['openid']
    
    created = Comments.objects.create(
        wxuser=WxUser.objects.get(user_openid=openid),
        comment_text=comment_text,
        item_id=item_id,
    )
    

    return Response(data={'code':200,'msg':'ok','data':{}})









@csrf_exempt 
@api_view(['GET'])
@authentication_classes([])
def payOrder(request):
    import time
    JSCODE=''
    if request.method == 'GET':
        
        item_price = request.GET.get('item_price')
        num_buy = int(request.GET.get('num_buy'))
        reward =  request.GET.get('reward')
        price = request.GET.get('total_fee')

        #获取客户端ip
        client_ip,port=request.get_host().split(":")
        
 
        #获取小程序openid
        JSCODE = request.GET.get('code')
        ####print('JSCODE',JSCODE)
        appid= 'wxd647f4c25673f368'
        secret='7de75de46a3d82dcc0bed374407f310f'
        wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
        res = json.loads(requests.get(wxLoginURL).content)
        if 'errcode' in res:
            return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
        openid=res['openid']
        ##print('openid',openid)


 
        #请求微信的url
        url= 'https://api.mch.weixin.qq.com/pay/unifiedorder'
 
        #拿到封装好的xml数据
        ##print('bodtdata_input:',openid,'ip',client_ip,'price:',price)
        body_data=pay.get_bodyData(openid,client_ip,price)
        #print('body_data',body_data)
 
        #获取时间戳
        timeStamp=str(int(time.time()))
        #print('timeStamp',timeStamp)
 
        #请求微信接口下单
        respone=requests.post(url,body_data.encode("utf-8"),headers={'Content-Type': 'application/xml'})

 
        #回复数据为xml,将其转为字典
        content=pay.xml_to_dict(respone.content)

        #print("content:",content)
        
 
        if content["return_code"]=='SUCCESS':
            #获取预支付交易会话标识
            prepay_id =content.get("prepay_id")
            #获取随机字符串
            nonceStr =content.get("nonce_str")
 
            #获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign=pay.get_paysign(prepay_id,timeStamp,nonceStr)

            #print("paysign",paySign)
 
            #封装返回给前端的数据
            data={"prepay_id":prepay_id,"nonceStr":nonceStr,"paySign":paySign,"timeStamp":timeStamp}
 
            return HttpResponse(packaging_list(data))
 
        else:
            #print('支付失败')
            return HttpResponse("请求支付失败")

def pay_feedback(request):
    


    return HttpResponse('test')
    #print("Pay_success",request)




@csrf_exempt 
@api_view(['GET'])
@authentication_classes([])
def weChatPay(request):
    mch_id='1560463491'
    mch_key='qingjiaorenlingshop2019111820000'
    code= request.GET.get('code')
    item_id=request.GET.get('item_id')
    item_name = request.GET.get('item_name')
    item_price = request.GET.get('item_price')
    num_buy = int(request.GET.get('num_buy'))
    reward =  request.GET.get('reward')
    price = int(request.GET.get('total_fee'))*100
    address= request.GET.get('address')
    nickname=request.GET.get('nickname')
    post_sign =request.GET.get('post_sign')
    name_rec=request.GET.get('name_rec')
    phone_num = request.GET.get('phone_num')
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'
    NOTIFY_URL='https://qingjiao.shop/dataserver/pay_feedback'
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    nonceStr = pay.getNonceStr()
    if 'errcode' in res:
        return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
    openid=res['openid']

    wepy_order =  WeChatPay(appid=appid,sub_appid=appid,api_key=mch_key,mch_id=mch_id)
    pay_res = wepy_order.order.create(
        trade_type="JSAPI",
        body=item_name,
        total_fee=price,
        notify_url=NOTIFY_URL,
        user_id=openid,
        out_trade_no=pay.getWxPayOrdrID(),
    )
    #print("------pay_res",pay_res)
    prepay_id = pay_res.get("prepay_id")
    
    wepy_sign=wepy_order.order.get_appapi_params(prepay_id=prepay_id)
    #print('------wepy_sign:',wepy_sign)

    timeStamp=str(int(time.time()))
    nonceStr=pay_res['nonce_str']
    paySign=pay.get_paysign(prepay_id=prepay_id,timeStamp=timeStamp,nonceStr=nonceStr)
    #print("------paySign:",paySign)

    return Response(data={'wepy_sign':wepy_sign,'status':100,'paySign':paySign,'timeStamp':timeStamp,'nonceStr':nonceStr})



    



#def get_questions():



#def data_response():

#def get_wxuser(request):

