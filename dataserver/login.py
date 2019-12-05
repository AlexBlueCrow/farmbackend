import hashlib
import json
import requests
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.response import Response
from django_redis import get_redis_connection
from .models import WxUser
from .serializers import WxUserSerializer




@api_view(['POST'])
@authentication_classes([]) # 添加

def wx_login(request):
    print('request',request)
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'

    JSCODE = request.data['code']

    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return Response(data={'code':res['errcode'],'msg':res['errmsg']})
    ##success
    openid=res['openid']
    session_key=res['session_key']
    print('openid:',openid)
    user,created = WxUser.objects.get_or_create(

        user_openid=openid,          
    )
    user_str = str(WxUserSerializer(user).data)
    print('user_ste:',user_str)
    print('user:',user)
    print('response:',res)

        ##定义登录
    sha=hashlib.sha1() 
    sha.update(openid.encode())
    sha.update(session_key.encode())
    digest = sha.hexdigest()
 

       #存入缓存，有效期2小时
    conn = get_redis_connection('default')
    conn.set(digest, user_str, ex=2*60*60)
    return Response(data={'code':200,'msg':'ok','data':{'skey':digest}})
 
@api_view(['POST'])
@authentication_classes([]) # 添加
def wx_update(request):
    appid= 'wxd647f4c25673f368'
    secret='7de75de46a3d82dcc0bed374407f310f'

    JSCODE = request.data['code']

    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return Response(data={'code':res['errcode'],'msg':res['errmsg']})
    ##success
    openid=res['openid']
    session_key=res['session_key']
    user = WxUser.objects.get_or_create(

        user_openid=openid,          
    )
    cityName = request.data['cityName']
    countyName = request.data['countyName']
    detailInfo = request.data['detailInfo']
    provinceName = request.data['provinceName']
    
    address = provinceName+countyName+cityName+detailInfo
    phoneNum = request.data['phoneNum']
    addressee = request.data['userName']
    user.user_address = address
    user.user_phonenumber = phoneNum
    user.user_addressee = addressee
    user.save()

    
    user_str = str(WxUserSerializer(user).data)
    return Response(data={'code':200,'msg':'ok'})

    


