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
from dataserver.models import WxUser,Item,FarmUser,Question,Order,Comments,Prepay_Order,Region,Varify_failed,CollectiveOrder,GiftCode
from dataserver.serializers import WxUserSerializer,ItemSerializer,OrderSerializer,FarmUserSerializer,QuestionSerializer,CommentsSerializer,Prepay_OrderSerializer,RegionSerializer,CollectiveOrderSerializer,GiftCodeSerializer
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
import operator
from math import radians, cos, sin, asin, sqrt
import random,string
from django.core.serializers.json import json
import csv



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

    items = Item.objects.filter(active = True)
    items_serializer = ItemSerializer(items,many=True)

    if request.GET.get('lon')=='undefined':
        return JSONResponse(items_serializer.data)

    ##Rearrange by distance
    userlon=float(request.GET.get('lon'))
    userlat=float(request.GET.get('lat'))
    Locdic = getFarmLocs()
    for item in items_serializer.data:
        farmid = item['owner']
        for Loc in Locdic:
            if Loc['id']==farmid:
                farmLon = Loc['loc']['lon']
                farmLat = Loc['loc']['lat']
                break
        item['dis']= round(getDistance(userlon,userlat,farmLon,farmLat),2)
    sorteddata= sorted(items_serializer.data,key=lambda x:x['dis'])
    return JSONResponse(sorteddata)

def getFarmLocs():
    farms= FarmUser.objects.all()
    dic = [] 
    for farm in farms:
        LocInfo = {'id':farm.id,'loc':{"lon":farm.longitude,"lat":farm.latitude}}
        dic.append(LocInfo)
    return dic

def getDistance(userLon,userLat,farmLon,farmLat):
    lon1, lat1, lon2, lat2 = map(radians, [userLon, userLat, farmLon, farmLat])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    s = c*r
    return s 


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
    orders = Order.objects.filter(wxuser=wxuser).order_by('-num')
    if orders:
        orders_serializer = OrderSerializer(orders,many=True)
        for order in orders_serializer.data:
            item = Item.objects.get(id=order['item'])
            order['item_name']=item.item_name
            order['farm_name']=item.owner.farm_name
            order['effect_time']=order['effect_time'][0:10]
            order['order_tree_ip']=order['tree_ip']
            order['order_buyernickname']=order['buyernickname']
            order['order_postsign']=order['postsign']
        
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
    AccTokUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret
    accToken = json.loads(requests.get(AccTokUrl).content)['access_token']
    
    
    SensCheckUrl = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token='+accToken
    data = "{'content':comment_text}"
    r = json.loads(requests.post(SensCheckUrl,data=data).content)

    

    if r['errcode']=='87014':
        

        return JSONResponse({'code':'sensitive'})
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
    openid=res['openid']
    if comment_text:
        created = Comments.objects.create(
            wxuser=WxUser.objects.get(user_openid=openid),
            comment_text=comment_text,
            item_id=item_id,
        )
    
    

    return Response(data={'code':'success','msg':'ok','data':{}})









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

    mch_id='1571816511'
    mch_key='qingjiaorenlingshop2019111820000'
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'


    code= request.GET.get('code')
    item_id=request.GET.get('item_id')
    item_name = request.GET.get('item_name')
    item_price = request.GET.get('item_price')
    num_buy = int(request.GET.get('num_buy'))
    reward =  request.GET.get('reward')
    price = int(float(request.GET.get('total_fee'))*100)
    address= request.GET.get('addRegion')+request.GET.get('addDetail')
    nickname=request.GET.get('nickname')
    post_sign =request.GET.get('post_sign')
    name_rec= request.GET.get('name_rec')
    phone_num = request.GET.get('phone_num')
    tree_ip = get_treeip(item_id)

    
    NOTIFY_URL='https://qingjiao.shop:8000/dataserver/pay_feedback'
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    nonceStr = pay.getNonceStr()
    if 'errcode' in res:
        return Response(data={'code':response['errcode'],'msg':response['errmsg']})
    ##success
    openid=res['openid']
    wxuser = WxUser.objects.get_or_create(
        user_openid=openid,
    )
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
    
    
    prepay_id = pay_res.get("prepay_id")
    wepy_sign=wepy_order.order.get_appapi_params(prepay_id=prepay_id)
    

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
        phone_num = str(phone_num),
        name_rec = name_rec,
    )
    #print("------paySign:",paySign)

    return Response(data={'wepy_sign':wepy_sign,'status':100,'paySign':paySign,'timeStamp':timeStamp,'nonceStr':nonceStr})



@csrf_exempt 
def pay_feedback(request): 
    mch_id='1571816511'
    mch_key='qingjiaorenlingshop2019111820000'
    appid= 'wxd647f4c25673f368'
    
    xml = request.body.decode('utf-8')
    

    wepy_order =  WeChatPay(appid=appid,sub_appid=appid,api_key=mch_key,mch_id=mch_id)
    result = wepy_order.parse_payment_result(xml)
    #print('pay_result:',result)
    

    prepay = Prepay_Order.objects.get(out_trade_no=result['out_trade_no'])
    prepay_serializer = Prepay_OrderSerializer(prepay,many=False)
    #print('prepay_serializer',prepay_serializer.data)
    if prepay_serializer.data['varified']==True:
        #print('varified==True')
        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
   
    #print('fee,',float(prepay_serializer.data['fee']),float(result['total_fee']))
    if (float(prepay_serializer.data['fee'])*100 == float(result['total_fee'])):
        #print('sign=sign&fee=fee')
        item = Item.objects.get(id=prepay_serializer.data['item_id'])
        wxuser = WxUser.objects.get(user_openid=prepay_serializer.data['openid'])
        item_serializer = ItemSerializer(item,many=False)
        

        new_tree = get_treeip(item_id=item.id)
        region_name=new_tree["region_name"]
        r=new_tree['row']
        l=new_tree['line']
        i=new_tree['i']
        
        tree_ip= region_name+"-"+str(l)+'行'+str(r)+"列"
        update_region_status(region_name=region_name,r=r,l=l,new_status=1,i=i)
        
        new_order = Order.objects.create(
            num = str(prepay_serializer.data['out_trade_no']),
            item = item,
            wxuser = wxuser,
            deliver_address = prepay_serializer.data['deliver_address'],
            price_paid = prepay_serializer.data['fee'],
            quantity = prepay_serializer.data['quantity'],
            buyernickname = prepay_serializer.data['buyernickname'],
            postsign = prepay_serializer.data['postsign'],
            price_origin = item_serializer.data['item_price'],
            tree_ip = tree_ip,
            benefit = item_serializer.data['item_benefit'],
            guaranteed = item_serializer.data['item_guaranteed'],
            imageUrl = item_serializer.data['pic_address'],
            phone_num = str(prepay_serializer.data['phone_num']),
            name_rec = prepay_serializer.data['name_rec'],
            ip_row=r,
            ip_line=l,
        )

        #print('order created:',new_order)

        prepay.varified = True
        prepay.save()
        

        #print('prepay varified')

        return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    else:
        failed = Varify_failed.objects.create(
            fee = prepay_serializer.data['fee'],
            out_trade_no=prepay_serializer.data['out_trade_no'],
        )
        return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[金额错误]]></return_msg></xml>')
    
    #print("Pay_success",request)

def get_treeip(item_id):
    item_id=item_id
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
            if status[i]=='0':            
                r = i%rows+1 
                l = i//rows+1
                tree_ip={
                    "region_name":region_name,
                    "row":r,
                    "line":l,
                    "i":i,
                }
                #print('tree_ip:',tree_ip)
                return tree_ip
            else:
                i=i+1      
    raise Exception("no_tree_available")

def update_region_status(region_name,r,l,new_status,i):
    
    region = Region.objects.get(region_name=region_name)
    rows= region.num_rows
    if(not i):
        i=rows*(l-1)+r-1
    old_code=region.status
    #print(old_code)
    new_code=old_code[:i]+str(new_status)+old_code[i+1:]
    #print(new_code)
    region.status=new_code
    region.save()
    return region.save()

def allorder(request):
    orders = Order.objects.all()
    orders_serializer = OrderSerializer(orders,many = True)
    for order in orders:
        print('商品名称',order.item.item_name,'昵称',order.buyernickname,'收件姓名',order.name_rec,"签名",order.postsign,'ip',order.tree_ip,'寄语',order.message_from_farm)
    
    


   
    return JSONResponse(orders_serializer)

def index(request):
    return render(request,'dataserver/index.html')
    
def gen_random_code(seed,length=10):
    prefix = hex(int(seed[2:]))
    length = length - len(prefix)

    chars=string.ascii_letters+string.digits
    code = prefix + ''.join([random.choice(chars) for i in range(length)])
    return code.upper()   


@csrf_exempt 
@api_view(['POST','GET'])
@authentication_classes([])
def gen_col_order(request):
    i=0
    buyer_name = request.GET.get('buyer_name')
    item_name = request.GET.get('item_name')
    num = request.GET.get('num')
    paid = request.GET.get('paid')
    contact= request.GET.get('contact')
    phone_num = request.GET.get('phone_num')
    
    item = Item.objects.get(item_name=item_name)
    
    
    code = gen_random_code(seed=phone_num,length =14)
    newdeal = CollectiveOrder.objects.create(
        code = code,
        companyname = buyer_name,
        contact = contact,
        phone_num = phone_num,
        price = paid,  
    )
    
    newdeal.save()
    
    while i<int(num):
        
        gen_gift_code(item_id=item.id,col_order=newdeal)
        i=i+1


    dealserializer = CollectiveOrderSerializer(newdeal,many = False)
    return JSONResponse(dealserializer.data)
    




def gen_gift_code(item_id,col_order):
    
    new_tree = get_treeip(item_id=item_id)
    region_name=new_tree["region_name"]
    r=new_tree['row']
    l=new_tree['line']
    i=new_tree['i']

    tree_ip= region_name+":"+str(l)+"x"+str(r)

    update_region_status(region_name=region_name,r=r,l=l,new_status=1,i=i)
    chars=string.ascii_letters+string.digits
    code =  ''.join([random.choice(chars) for i in range(12)])
    giftcode = GiftCode.objects.create(
        code = code,
        item_id=item_id,
        tree_ip = tree_ip,
        owner = col_order,
        ip_line=l,
        ip_row=r,
    )
    giftcode.save()

    return giftcode
    #print('order created:',new_order)

def usecode(request):
    code = request.GET.get('giftcode')
    if len(code) == 12:
        try:
            gcode = GiftCode.objects.get(code = code)
        except:
            return JSONResponse({'res':'error','errormsg':'wrong code'})
        if gcode.is_used:
            return JSONResponse({'res':'error','errormsg':'code used'})
        else:
            item = Item.objects.get(id = gcode.item_id)
            
            jsoninfo={
                'res':'varified',
                'item_id':gcode.item_id,
                'item_price':item.item_price,
                'item_name':item.item_name,
                'code':code
                
            }
            return JSONResponse(jsoninfo)  

    else :   
        if len(code) == 14:
            try:
                ccode = CollectiveOrder.objects.get( code = code)                
            except:                
                return JSONResponse({'res':'error','errormsg':'wrong code'})
            gcodes = GiftCode.objects.filter(owner = ccode)
            gcodes_serializer = GiftCodeSerializer(gcodes,many =True)
            return JSONResponse(gcodes_serializer.data)
        else:
            return JSONResponse({'res':'error','errormsg':'wrong code'})

def get_gift(request):
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'
    code = request.GET.get('code')
    giftcode = request.GET.get('giftcode')
    address = request.GET.get('addRegion')+request.GET.get('addDetail')
    nickname = request.GET.get('nickname')
    post_sign = request.GET.get('post_sign')
    name_rec = request.GET.get('name_rec')
    phone_num = request.GET.get('phone_num')
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+code+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    openid = res['openid']
    gcode = GiftCode.objects.get(code=giftcode)
    ccode = gcode.owner
    item = Item.objects.get(id = gcode.item_id)
    item_serializer = ItemSerializer(item,many = False)
    wxuser = WxUser.objects.get(
        user_openid=openid,
    )
    new_order = Order.objects.create(
            num = pay.getWxPayOrdrID(),
            item = item,
            wxuser = wxuser,
            deliver_address = address,
            price_paid = 0,
            quantity = 1,
            buyernickname = nickname,
            postsign = post_sign,
            price_origin = item_serializer.data['item_price'],
            tree_ip = gcode.tree_ip,
            benefit = item_serializer.data['item_benefit'],
            guaranteed = item_serializer.data['item_guaranteed'],
            imageUrl = item_serializer.data['pic_address'],
            phone_num = str(phone_num),
            name_rec = name_rec,
            ip_row=0,
            ip_line=0,
        )   
    gcode.is_used = True
    gcode.save()
    jsoninfo={
                'res':'success',
                'item_id':gcode.item_id,
                'item_price':item.item_price,
                'code':gcode.code,
                'item_name':item.item_name,
                'giver':ccode.companyname,
            }
    return JSONResponse(jsoninfo)
            

        
            
        
    
    

    






    







    



#def get_questions():



#def data_response():

#def get_wxuser(request):

