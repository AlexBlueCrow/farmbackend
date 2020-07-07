from django.shortcuts import render
from zxserver.models import ZxOrder,ZxItem,Captain,ZxUser,ZxOrder,ZxComments
from dataserver.models import FarmUser,WxUser,Region,Question,Item,Order,Comments,GiftCode
from zxserver.serializers import ZxOrderSerializer,ZxItemSerializer
from dataserver.serializers import FarmUserSerializer
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
import csv as csvreader
from rest_framework.authtoken.models import Token
from zxserver.views import JSONResponse
from .serializers import AdminUserSerializer
from .models import VideoFiles,PicFiles
from django.utils import timezone
# Create your views here.




def order(request):
    start=request.GET.get('date1')
    end=request.GET.get('date2')
    farm_name = request.GET.get('farmname')
    
    orders = ZxOrder.objects.filter(effect_time__range=(start,end),farm_name = farm_name)
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

    if request.method == 'GET':
        farmname = request.GET.get('farmname')
        try:
            farmuser = FarmUser.objects.get(farm_name=farmname)
            items = ZxItem.objects.filter(owner = farmuser)
            items_ser = ZxItemSerializer(items,many=True)
            return JSONResponse({'code':20000,'data':items_ser.data})
        except:
            return HttpResponse('农场未创建')
    return HttpResponse('something is wrong')


    if request.method == 'PUT':
        item_name = request.PUT.get('itemname')
        name = request.PUT.get('name')
        category = request.PUT.get('class')
        price = request.PUT.get('price')
        size = request.PUT.get('size')
        farmname = request.PUT.get('farmname')
        item_id = request.PUT.get('id')
        video_file = request.FILES.get('video')
        pic_file = request.FILES.get('pic')

        if video_file:
            video_pf=video_file.name.split('.')[-1]
            video_file.name = identifier + '.' + video_pf  
        if pic_file:
            pic_pf=pic_file.name.split('.')[-1]
            pic_file.name = identifier + '.' + pic_pf + str(timezone.localtime())
        identifier = farmuser.farm_name + '--' + item_name
        item = ZxItem.objects.get(id=item_id)
        static = StaticFiles.objects.get(identifier = identifier)
        
        
        
        
    

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({})




    
@csrf_exempt
def csv(request):
    if request.method == 'POST':
        csvfile = request.FILES.get('csvfile')
        name = csvfile.name
        csv_reader=csvreader.reader(open('homepage/csv/'+name,encoding='utf-8'))
        
        num=0
        titles=[]
        i=0
        for row in csv_reader:
            if num==0:
                
                for item in row:
                    titles.append(item)
                for item in titles:
        
                    i+=1
                num+=1
            else:
              pass
                #new = FarmUser.objects.create(
                #)
                #print(new)
                #new.save()

                
        return HttpResponse('good')
  
        
        
@csrf_exempt    
def Farm_API(request):
    if request.method=='GET':
        farmname = request.GET.get('farmname')
        farm_obj = FarmUser.objects.get(farm_name = farmname)
        farm_serializer = FarmUserSerializer(farm_obj,many=False)

        return JSONResponse({'code':20000,'data':farm_serializer.data})
    
    if request.method == 'POST':
   
        farmname = request.POST.get('farmname')
        
        address = request.POST.get('address')
        description = request.POST.get('description')
        phonenum = request.POST.get('phonenum')
        contact = request.POST.get('contact')
        farm_type = request.POST.get('type')
        
        
        fuser = FarmUser.objects.get(farm_name=farmname)
        fuser.farm_address = address
        fuser.farm_description = description
        fuser.farm_phonenumber = phonenum
        fuser.farm_contact = contact
        fuser.farm_type = farm_type
        fuser.save()
        msg1='info_update_success'
        logo = request.FILES.get('logo')
        

        

        
        msg = 'no_new_logo'
        if logo:
            logo_pf= logo.name.split('.')[-1]
            logo_fname = farmname+'-logo'+'.'+logo_pf
            logo.name = logo_fname
            identifier = farmname+'-logo'
            try:
                static= StaticFiles.objects.create(
                    identifier= identifier,
                    pic = logo,
                )
                msg = '头像创建成功'
                fuser.farm_log_address=logo_fname
                fuser.save()
            except:
                static = StaticFiles.objects.get(identifier=identifier)
                static.pic = logo
                
                static.save()
                msg = '头像更新成功'
                fuser.farm_logo_address=logo.name
                
                fuser.save()

        return JSONResponse({'code':20000,'data':{'res':msg1,'msg':msg},})

        