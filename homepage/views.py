from django.shortcuts import render
from zxserver.models import ZxOrder,ZxItem,Captain,ZxUser,ZxOrder,ZxComments
from dataserver.models import FarmUser,WxUser,Region,Question,Item,Order,Comments,GiftCode
from zxserver.serializers import ZxOrderSerializer,ZxItemSerializer
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

# Create your views here.




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

    if request.method == 'GET':
        farmname = request.GET.get('farmname')
        try:
            famruser = FarmUser.objects.get(farm_name=farmname)
            items = ZxItem.objects.filter(owner = farmuser)
            items_ser = ZxItemSerializer(items,many=true)
            print(items_ser)
            return JSONResponse(items_ser.data)

        except:
            return HttpResponse('农场未创建')

    

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({})




    
@csrf_exempt
def csv(request):
    if request.method == 'POST':
        print('request get')
        csvfile = request.FILES.get('csvfile')
        print(csvfile)
        name = csvfile.name
        print('name:',name)
        
        csv_reader=csvreader.reader(open('homepage/csv/'+name,encoding='utf-8'))
        print('reader',csv_reader)
        num=0
        titles=[]
        i=0
        for row in csv_reader:
            if num==0:
                print('0000')
                for item in row:
                    titles.append(item)
                for item in titles:
                    print(item+' = '+'row['+str(i)+'],')
                    i+=1
                num+=1
            else:
              pass
               
                #new = FarmUser.objects.create(
                    
                #)
                #print(new)
                #new.save()

                
        return HttpResponse('good')
    else:
        print('what?')
        
        
        