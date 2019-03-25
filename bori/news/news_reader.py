import feedparser

from ..news_finder import NewsFinder
from ..twitter_reader import TwitterReader
from ..utility import json_utility
from ..tasks import get_rcmd_news_list
from ..tasks import get_headline_news_list
from ..news import news_type

from django.core import serializers

import coloredlogs, logging


logger = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG', logger= logger)




class NewsReader():
    
    def __init__(self):
        self.json_utility = json_utility.JsonUtiilty()
        self.twitter_reader = TwitterReader(twt_number=2)
        self.news_type = news_type.NewsType()
 
    def get_recommend_news(self, user):
        user_tweets = self.twitter_reader.read_user_tweet(user)
        
        news_list = self.get_rcmd_news_list_none_task(user_tweets)
        
        news_dict = self.json_utility.make_json_array_for_rcmd_news(news_list) #make_json_array_for_rcmd_news(news_list)
        
        return news_dict

    def get_recommend_news_from_db(self, user):
        user_tweets = self.twitter_reader.read_user_tweet(user)
        news_list = []
        news_dict = {}
        
        query_list = self.get_rcmd_news_list_none_task(user_tweets)

        for querySet in query_list:
            
            if not querySet:
                continue
                
            for item in querySet:
                #logger.debug("item: %s" % item)
                temp_dict = self.makeDictionary(item)
                news_list.append(temp_dict)
                
        news_dict['news_type'] = self.news_type.KEY_RECOMMEND_NEWS
        news_dict['news_list'] = news_list
        
        return news_dict
    
    def makeDictionary(self, item):
        news_dict = {
        "link" : item.link,
        "id" :item.news_id,
        "source" : item.source,
        "title" :item.title,
        "published_parsed" : item.published_date,
        "media_content" :item.media_content,
        "category" :item.news_category,
        }
        
        return news_dict


    def get_headline_news(self):
        url = 'https://news.google.com/news/rss/?hl=ko&gl=KR&ned=kr'
        news_list = feedparser.parse(url)
        entries = news_list['entries']

        news_dict = self.json_utility.make_json_array_for_headline_news(entries)
       
        return news_dict


    def get_rcmd_news_list_none_task(self, user_tweets):
        news_finder = NewsFinder()
        news_list = news_finder.find_most_sim_news(user_tweets)
        
    
        return news_list

    def get_headline_news_with_celery(self):

        #news_list = self.none_task_get_headline_news_list()
        result = get_headline_news_list.delay()
      
        try:
            news_list = result.get()
        except Exception as exc:
            logger.debug('head news Exception!!!' + str(exc))
            logger.debug("traceback %s:", result.traceback)

            result.revoke()
            
            news_dict = {}
            return news_dict

        entries = news_list['entries']

        news_dict = self.json_utility.make_json_array_for_headline_news(entries)

        status = result.ready()
        if(status):
            print('head news excuted!!')
        else:
            print('not ready!!!!')


        return news_dict
       
    def get_rcmd_news_with_celery(self,user):
        
        
        user_tweets = self.twitter_reader.read_user_tweet(user)
        result = get_rcmd_news_list.delay(user_tweets)

        try:
            news_list  = result.get()
        except Exception as exc:
            logger.debug('rcmd news Exception!!!' + str(exc))
            logger.debug("traceback %s:", result.traceback)

            result.revoke()
            
            news_dict = {}
            return news_dict
        

        _news_dict = self.json_utility.make_json_array_for_rcmd_news(news_list)

        status = result.ready()
        if(status):
            print('rcmd news excuted!!')
        else:
            print('not ready!!!!')
            
        return _news_dict
