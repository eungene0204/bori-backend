import json
from ..news import news_type

import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class JsonUtiilty():
    

    def __init__(self):
        self.news_type = news_type.NewsType()
        
        
    def make_json_array_for_rcmd_news(self, news_list ):
        
        news_dict = {}
        _news_list =[]

        for news in news_list:
            for news_info in news:
        
                news_info = json.dumps(news_info)
                news_info = json.loads(news_info)
        
                _news_list.append(news_info)
                
        logger.info("Size of all news list %s:", len(_news_list))
       
        news_dict['news_type'] = self.news_type.KEY_RECOMMEND_NEWS
        news_dict['news_list'] = _news_list
        
        
        return news_dict
    
    

    def make_json_array_for_headline_news(self,entries):
        news_dict = {}
        news_list =[]

        for news_info in entries:
            #print('news_info tyep:', type(news_info))
            news_info = json.dumps(news_info)
            news_info = json.loads(news_info)
            #print('news_info:', news_info)
            news_list.append(news_info)
        
        news_dict['news_type'] = self.news_type.KEY_HEAD_LINE_NEWS
        news_dict['news_list'] = news_list

        return news_dict


        
        

