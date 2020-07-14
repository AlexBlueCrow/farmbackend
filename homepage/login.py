from rest_framework.views import APIView
from rest_framework.response import Response
from dataserver.models import FarmUser
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .models import StaticFiles,AdminUser
import jwt
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token
from zxserver.views import JSONResponse
from .serializers import AdminUserSerializer



   

@csrf_exempt
def register(request):
    username = request.POST.get('username')
    password=request.POST.get('password')
    phone_number=request.POST.get('phone_number')
    farmname=request.POST.get('farmname')
    name = request.POST.get('name')
    
    try:
        fuser = Farmuser.objects.get(farm_name=farmname)
        if fuser:
            return HttpResponse('农场已创建账号')
    except:
        pass
    try:
        new = AdminUser.objects.create(
            username=username,
            password= password,
            phonenumber=phone_number,
            farm = farmname,
            name = name,
            role = 'farmuser'
        )
        token = Token.objects.create(user=new)
        token.save()
        
        return HttpResponse('注册成功')
    except:
        return HttpResponse('用户名或手机号已被注册，请重试')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        username = body['username']
        password = body['password']
        
        user_obj = AdminUser.objects.filter(username=username,password=password).first()
        
        if user_obj:
            token = Token.objects.get(user=user_obj)
           
            return JSONResponse({'code':20000,'token':token.key,'msg':'登录成功'})
        else:
            return HttpResponse('用户名或密码错误')


@csrf_exempt
def userInfo(request):
    
    if request.method == 'GET':
        token = request.GET.get('token')
       
        try:
            token_obj = Token.objects.get(key=token)
        except:
            return HttpResponse('身份验证失败')
        user = AdminUser.objects.get(id=token_obj.user_id)
      
        user_ser = AdminUserSerializer(user).data
        
        return JSONResponse({'code':20000,'data':user_ser})

        