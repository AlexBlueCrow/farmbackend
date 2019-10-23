
import hashlib
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import Response
from dataserver.models import WxUser,Item,FarmUser,Question,Order
from dataserver.serializers import WxUserSerializer,ItemSerializer,OrderSerializer,FarmUserSerializer,QuestionSerializer
from rest_framework.decorators import api_view, authentication_classes
from django_redis import get_redis_connection

@api_view(['POST'])
@authentication_classes([]) # 添加



# Create your views here.


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs) 

def get_farmuser(request):
    farmuser = FarmUser.objects.all()
    farmuser_serializer = FarmUserSerializer(farmuser,many=True)
    return JSONResponse(farmuser_serializer.data)

def get_item(request):
    pk=request.GET.get('pk')
    try:
        item = Item.objects.all()
    except Item.DoesNotExist:
        pk=1
        item = Item.objects.get(id=pk)
    print(item)
    item_serializer = ItemSerializer(item,many=True)
    print(item_serializer.data)
    return JSONResponse(item_serializer.data)

def get_questions(request):
    item_id=request.GET.get('item_id')
    print(item_id)
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return HttpResponseNotFound
    print(item)
    questions = Question.objects.all()
    print(questions)
    
    questions_serializer = QuestionSerializer(questions,many=True)
    return JSONResponse(questions_serializer.data)
    

   



#def get_questions():

#def get_farmuser():

#def data_response():

#def get_wxuser(request):
    
