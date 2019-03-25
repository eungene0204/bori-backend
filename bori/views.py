import logging
import sys

import jpype
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .news import news_reader
from .models import RcmdNews
from .serializers import RcmdNewsSerializer
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from rest_framework import generics

import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

newsReader = news_reader.NewsReader()

#jpype.attachThreadToJVM()

class RcmdNewsListAPI(generics.ListAPIView):
    queryset = RcmdNews.objects.all()
    serializer_class = RcmdNewsSerializer

class RcmdDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = RcmdNews.objects.all()
    serializer_class = RcmdNewsSerializer


class RcmdNewsListView(ListView):
    model = RcmdNews
    
class RcmdNewsListCreateView(CreateView):
    model = RcmdNews
    fields = ['news_id', 'title', 'link', 'published_date', 'media_contetn', 'news_category']



@csrf_exempt
def head(request):
    logger.info('head view')
    
    #news_dict = newsReader.get_headline_news_with_celery()
    news_dict = newsReader.get_headline_news()

    return JsonResponse(news_dict)

@csrf_exempt
def rcmd(request):
    logger.info('rcmd view')

    json_data = json.loads(request.body.decode('utf-8'))
    user = json_data['screenName']
    logger.info("user name:%s", user)
    
    #news_dict = newsReader.get_rcmd_news_with_celery(user)
    #news_dict = newsReader.get_recommend_news(user)
    
    news_dict = newsReader.get_recommend_news_from_db(user)

    return JsonResponse(news_dict)


