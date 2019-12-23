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
        return HttpResponse(res['errcode'])
    openid=res['openid']
    wxuser = WxUser.objects.get(user_openid=openid)
    orders = Order.objects.filter(order_wxuser=wxuser)
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

def get_userInfo(request):
    code = request.GET.get('code')
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    openid=res['openid']
    wxuser = WxUser.objects.get(user_openid=openid)
    wxuser_serializer = WxUserSerializer(wxuser,many=False)
    return JSONResponse(wxuser_serializer.data)




    

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







@csrf_exempt 
@api_view(['GET'])
@authentication_classes([])
def weChatPay(request):
    mch_id='1560463491'
    mch_key='qingjiaorenlingshop2019111820000'
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'
    code= request.GET.get('code')
    item_id=request.GET.get('item_id')
    item_name = request.GET.get('item_name')
    item_price = request.GET.get('item_price')
    num_buy = int(request.GET.get('num_buy'))
    reward =  request.GET.get('reward')
    price = int(request.GET.get('total_fee'))*100
    address= request.GET.get('addRegion')+request.GET.get('addDetail')
    nickname=request.GET.get('nickname')
    post_sign =request.GET.get('post_sign')
    name_rec= request.GET.get('name_rec')
    phone_num = request.GET.get('phone_num')
    
    NOTIFY_URL='https://qingjiao.shop:8000/dataserver/pay_feedback'
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    nonceStr = pay.getNonceStr()
    if 'errcode' in res:
        return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
    openid=res['openid']

    wepy_order =  WeChatPay(appid=appid,sub_appid=appid,api_key=mch_key,mch_id=mch_id)
    out_trade_no=pay.getWxPayOrdrID()
    pay_res = wepy_order.order.create(
        trade_type="JSAPI",
        body=item_name,
        total_fee=price,
        notify_url=NOTIFY_URL,
        user_id=openid,
        out_trade_no=out_trade_no,
    )
    #print("------pay_res",pay_res)
    prepay_id = pay_res.get("prepay_id")
    wepy_sign=wepy_order.order.get_appapi_params(prepay_id=prepay_id)
    #print('------wepy_sign:',wepy_sign)

    timeStamp=str(int(time.time()))
    nonceStr=pay_res['nonce_str']
    paySign=pay.get_paysign(prepay_id=prepay_id,timeStamp=timeStamp,nonceStr=nonceStr)
    prepay_order = Prepay_Order.objects.create(
        out_trade_no = out_trade_no,
        sign = paySign,
        noncestr=nonceStr,
        openid=openid,
        fee = int(price)/100,##cents
        deliver_address = address,
        quantity = num_buy,
        buyernickname = nickname,
        postsign = post_sign,
        item_id = int(item_id),
    )
    #print("------paySign:",paySign)

    return Response(data={'wepy_sign':wepy_sign,'status':100,'paySign':paySign,'timeStamp':timeStamp,'nonceStr':nonceStr})


@csrf_exempt 
def pay_feedback(request): 
    mch_id='1560463491'
    mch_key='qingjiaorenlingshop2019111820000'
    appid= 'wxd647f4c25673f368'
    print("info:------------------------")
    xml = request.body.decode('utf-8')
    print("xml:-------------------------",xml)  

    wepy_order =  WeChatPay(appid=appid,sub_appid=appid,api_key=mch_key,mch_id=mch_id)
    result = wepy_order.parse_payment_result(xml)
    print('pay_result:',result)
    

    prepay = Prepay_Order.objects.get(out_trade_no=result['out_trade_no'])
    prepay_serializer = Prepay_OrderSerializer(prepay,many=False)
    print('prepay_serializer',prepay_serializer.data)
    if prepay_serializer.data['varified']==True:
        print('varified==True')
        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
   
    print('fee,',float(prepay_serializer.data['fee']),float(result['total_fee']))
    if (float(prepay_serializer.data['fee'])*100 == float(result['total_fee'])):
        print('sign=sign&fee=fee')
        item = Item.objects.get(id=prepay_serializer.data['item_id'])
        wxuser = WxUser.objects.get(user_openid=prepay_serializer.data['openid'])
        item_serializer = ItemSerializer(item,many=False)
        


        new_order = Order.objects.create(
            order_num = str(prepay_serializer.data['out_trade_no']),
            order_item = item,
            order_wxuser = wxuser,
            order_deliver_address = prepay_serializer.data['deliver_address'],
            order_price_paid = prepay_serializer.data['fee'],
            order_quantity = prepay_serializer.data['quantity'],
            order_buyernickname = prepay_serializer.data['buyernickname'],
            order_postsign = prepay_serializer.data['postsign'],
            order_price_origin = item_serializer.data['item_price'],
            ##order_tree_ip = get_treeip(),
            order_benefit = item_serializer.data['item_benefit'],
            order_guaranteed = item_serializer.data['item_guaranteed'],
        )

        print('order created:',new_order)

        prepay.varified = True
        prepay.save()
        

        print('prepay varified')

        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    else:
        return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[金额错误]]></return_msg></xml>')
    
    #print("Pay_success",request)

def get_treeip(item_id):
    item_id=item_id.GET.get('item_id')
    
    item = Item.objects.get(id=item_id)
   
    regions = Region.objects.filter(item=item)
    
    regions_serializer = RegionSerializer(regions,many=True)
    for region in regions_serializer.data:
        rows = region['num_rows']
        lines = region['num_lines']
        status =  region['status']
        region_name=region['region_name']
        i=0 
        while i<rows*lines:
            if status[i]==0:
                status[i] = 1
                r = i//lines
                l = i%lines
                tree_ip={
                    "region_name":region_name,
                    "row":r,
                    "line":l,
                }
                tree_ip=dumps(treeip,indent=4)
                print(tree_ip)
                return JSONResponse(tree_ip)
            else:
                i=i+1
        

                    
        
    
    print("region_ser.data:",region_serializer.data)
    return JSONResponse(region_serializer.data)






    







    



#def get_questions():



#def data_response():

#def get_wxuser(request):

