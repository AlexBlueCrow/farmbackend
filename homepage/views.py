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
from .models import StaticFiles
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
        
        static= StaticFiles.objects.create(
            item_name= item_name,
            pic = pic_file,
            video = video_file,
        )
        
        created = ZxItem.objects.create(
            item_name=item_name,
            owner = farmuser,
            category = category,
            item_price = price,
            unit = size,
            video_address = static.video,
            pic_address = static.pic,
        )
        created.save()
        return HttpResponse('success')
    

    return HttpResponse('something is wrong')
    

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({})



