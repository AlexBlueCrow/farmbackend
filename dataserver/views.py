
from django.shortcuts import render
import requests
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
        item = Item.objects.filter(id=pk)
    except Item.DoesNotExist:
        pk=1
        item = Item.objects.get(id=pk)
    print(item)
    item_serializer = ItemSerializer(item,many=True)
    print(item_serializer)
    return JSONResponse(item_serializer.data)

def get_questions(request):
    id=request.GET.get('item_id')
    print(id)
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponseNotFound
    questions = Question.objects.filter(question_item=item)
    print(questions)
    questions_serializer = QuestionSerializer(questions,many=True)
    return JSONResponse(questions_serializer.data)
    

   


def login(request):
    appid= 'wx48c0b0d820c4563d'
    secret='4acdae8837a2d8e8a6a675193394eed1'
    JSCODE = request.GET.get('code')
    if JSCODE:
        wxLoginURL = 'https://api.weixin.qq.com/sns/jscode2session?' +'appid='+appid+'&secret='+secret+'&js_code='+JSCODE+'&grant_type='+'authorization_code'
        r = requests.get(wxLoginURL)
        print('response:',r.content)
        data = requests.get
        return HttpResponse(r)
    else:
        return HttpResponseNotFound
#def get_questions():

#def get_farmuser():

#def data_response():

#def get_wxuser(request):
    
