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
    appid= 'wx48c0b0d820c4563d'
    secret='4acdae8837a2d8e8a6a675193394eed1'
    JSCODE = request.data['code']
    print(JSCODE)
    wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
    res = json.loads(requests.get(wxLoginURL).content)
    if 'errcode' in res:
        return Response(data={'code':response['errcode'],'msg':response['errmsg']})
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

        ##定义登录态

    sha=hashlib.sha1()
    print(sha)
    sha.update(openid.encode())
    print(sha)
    sha.update(session_key.encode())
    print(sha)
    digest = sha.hexdigest()
    print(digest)

        

       #存入缓存，有效期2小时
    conn = get_redis_connection('default')
    conn.set(digest, user_str, ex=2*60*60)
    return Response(data={'code':200,'msg':'ok','data':{'skey':digest}})
 


