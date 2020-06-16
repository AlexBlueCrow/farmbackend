from django.shortcuts import render
from zxserver.models import ZxOrder,ZxItem
from dataserver.models import FarmUser
from zxserver.serializers import ZxOrderSerializer
from django.http import HttpResponse,HttpResponseNotFound
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from farmbackend.settings import MEDIA_ROOT,MEDIA_URL
from .models import StaticFiles,AdminUser
import jwt
from rest_framework_jwt.settings import api_settings
# Create your views here.



class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs) 


def order(request):
    start=request.GET.get('date1')
    end=request.GET.get('date2')
    farm_name = request.GET.get('farmname')
    orders = ZxOrder.objects.filter(effect_time__range=(start,end))
    orders_serializer = ZxOrderSerializer(orders,many=True)
    return JSONResponse(orders_serializer.data)

@csrf_exempt
def ZxItem_API(request):

    if request.method == 'POST':
        
        video_file = request.FILES.get('video')
        pic_file = request.FILES.get('pic')
        
        contact = request.POST
        
        item_name = request.POST.get('itemname')
        name = request.POST.get('name')
        category = request.POST.get('class')
        price = request.POST.get('price')
        size = request.POST.get('size')
        farmname = request.POST.get('farmname')

        
    
        
        try:
            farmuser = FarmUser.objects.get(farm_name=farmname)
        except:
            return HttpResponse('该农场不在系统中，请先创建农场')
        ##rename files with farm_name and item_name

        pic_pf=pic_file.name.split('.')[-1]
        video_pf=video_file.name.split('.')[-1]
        identifier= farmuser.farm_name+'--'+item_name
        pic_file.name= identifier+'.'+pic_pf
        video_file.name= identifier+'.'+video_pf
        try:
            static= StaticFiles.objects.create(
                identifier= identifier,
                pic = pic_file,
                video = video_file,
            )
        except:
            return HttpResponse('同名商品已存在')
        
        
        created = ZxItem.objects.create(
            item_name=item_name,
            owner = farmuser,
            category = category,
            item_price = price,
            unit = size,
            video_address = video_file.name,
            pic_address = pic_file.name,
        )
        created.save()
        return HttpResponse('success')
    

    return HttpResponse('something is wrong')
    

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({})

def login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    print(username,password)
    try:
        account = AdminUser.objects.get(username=username)
        if account.password == password:
             encoded_jwt = jwt.encode({'username':username},'secret_key',algorithm='HS256')
             return 

        else:
            return HttpResponse('用户名或密码错误')
    except:
        return HttpResponse('用户名或密码错误')


