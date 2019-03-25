# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals
import feedparser
from .news_finder import NewsFinder
from celery import shared_task, task
from .twitter_reader import TwitterReader

from celery.utils.log import get_task_logger
from requests import ConnectionError

logger = get_task_logger(__name__)


@task()
def my_print():
    print('hello world')
    
    

@shared_task(name='read_tweets')
def read_tweets(user):
    twt_number = 2
    twitter_reader = TwitterReader(twt_number)
    user_tweets = twitter_reader.read_user_tweet(user)
    
    return user_tweets

@shared_task(name='get_headline_news_list', queue = 'head_news')
def get_headline_news_list():
    
    logger.info('head news task')
    url = 'https://news.google.com/news/rss/?hl=ko&gl=KR&ned=kr'
    news = feedparser.parse(url)
   
    
    #print('get Headline news!!!: ', news)
    
    return news

@shared_task(name='get_rcmd_news_list', queue = 'rcmd_news' )
def get_rcmd_news_list(user_tweets):
    
    logger.info('rcmd task')
    print('rcmd task')
    
    news_finder = NewsFinder()

    '''
     try:
        news_list = news_finder.find_most_sim_news(user_tweets)
    except ConnectionError as exc:
        self.retry(exc=exc)
    
    news_list = list(news_list)
    
    '''
    news_list = news_finder.find_most_sim_news(user_tweets)
    
    news_list = list(news_list)
   
    return news_list

