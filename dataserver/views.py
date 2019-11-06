
import hashlib
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from dataserver.models import WxUser,Item,FarmUser,Question,Order
from dataserver.serializers import WxUserSerializer,ItemSerializer,OrderSerializer,FarmUserSerializer,QuestionSerializer


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
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        pk=1
        item = Item.objects.get(id=pk)
    print(item)
    item_serializer = ItemSerializer(item,many=False)
    print(item_serializer.data)
    return JSONResponse(item_serializer.data)

def get_questions(request):
    category=request.GET.get('cate')
    print("cate:",category)
    try:
        questions = Question.objects.filter(question_category=category)
        print(questions)
    except Question.DoesNotExist:

        return HttpResponseNotFound
    
    questions_serializer = QuestionSerializer(questions,many=True)
    return JSONResponse(questions_serializer.data)
    

   



#def get_questions():

#def get_farmuser():

#def data_response():

#def get_wxuser(request):
    
