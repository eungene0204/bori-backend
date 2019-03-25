from gensim.models import Word2Vec

from .utility import json_utility
from .word2vec_similarity import word2vec_similarity
from .rss_parser import rss_parser
from .hangul_util import hangul_util
from .word2vec_model import word2vec_model_reader

from multiprocessing import Pool

import pandas as pd
import os
import logging
import sys
import time
import multiprocessing
import coloredlogs

from bori import word2vec_model, word2vec_num_feature
import coloredlogs, logging

logger = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG', logger= logger)

'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

'''

from .models import RcmdNews


class NewsFinder():

    def __init__(self):
        self.module_dir = os.path.dirname(__file__)
        self.hangul_util = hangul_util()
        self.rss_parser = rss_parser()
        
        self.model = word2vec_model
        self.num_feature = word2vec_num_feature
        self.json_utility = json_utility.JsonUtiilty()
        
        #self.word2vec_model_reader = word2vec_model_reader.Word2VecModelReader()
        #self.model, self.num_feature = self.word2vec_model_reader.load_model()
        
        
    def read_objective_file(self):
        path = os.path.join(self.module_dir,'data','objective_words.csv')
        raw_words = pd.read_csv(path , header = 0, quoting=3, encoding='cp949',
                            error_bad_lines=False)
        
        values = raw_words.values

        objective_words=[]
        for word in values:
             objective_words.append(word[0])

        return objective_words

    def find_most_sim_news(self,user_tweets):
        
        mgr = multiprocessing.Manager()
    
        #news_info_list = mgr.list()
        
        news_info_list = []
        
        start_time = time.time()
        
        for twt_json in user_tweets:
           
            try:
                twt = twt_json['text']

                logger.debug('User tweet:%s', twt)
                twt = self.hangul_util.get_clean_hangul(twt)
                
                #not korean
                if(len(twt) <=0):
                    continue

                #p = multiprocessing.Process(target=self.get_news, args=(news_info_list,twt))
                #jobs.append(p)
                
                self.get_news_from_db(twt,news_info_list)

                logger.debug("news_info_list after db search %s" % news_info_list)
                
                if not news_info_list:
                    logger.info("No News in the DB")
                    self.serach_news(twt,news_info_list)

            except Exception as e:
                print(e)
        
        #for p in jobs:
            #p.start()
            
        end_time  = time.time() - start_time
        logger.debug('Time on finding News: %f'% end_time )

        return news_info_list

    def serach_news(self, twt, news_info_list):

        self.get_news_from_rss(twt, news_info_list)
        self.saveNewsList(news_info_list)
       
    def get_news_from_db(self,twt,new_info_list):
        category, similarity = self.get_twt_category_and_similarity(twt)
        
        filtered_news = RcmdNews.objects.filter(news_category = category)
        
        
        if filtered_news:
            new_info_list.append(filtered_news)

    def get_news_from_rss(self,twt, news_info_list):
        
        #p_name = multiprocessing.current_process().name
        #logger.debug('%s process start', p_name)
        
        category, similarity = self.get_twt_category_and_similarity(twt)
       
        #logger.debug('%s Tweet Category:%s',p_name, category)
        logger.debug('%s is in Category:%s',twt, category)
        
        #print(self.model.most_similar([avg_vector]))
   
        '''
        Finding News
        '''
        news = self.rss_parser.parse_feed_with_word(category)
    
        #logger.info('%s Number of News Entries: %d',p_name, len(news.entries))
        logger.info('Number of News Entries: %d', len(news.entries))

        self.checkNewsIsEmpty(news)
        news_info = self.rss_parser.get_news_info(news,category)
        
        news_info_list.append(news_info)
    
    def get_twt_category_and_similarity(self, twt):
        
        similarity_util = word2vec_similarity(self.model,self.num_feature)
        objective_words = self.read_objective_file()

        avg_vector = similarity_util.get_avg_vector(twt)
        
        similarity, category = \
            similarity_util.find_most_similar_category(avg_vector,objective_words)
        
        return category, similarity

    
    def checkNewsIsEmpty(self,news):
        #can't find news
        if(len(news.entries) == 0):
            logger.warning('There is no News!!!!!!')
            
            return

        
    def saveNewsList(self,news_info_list):
    
        news_id = ""
        link = ""
        source = ""
        title = ""
        published_date = ""
        media_content = ""
        news_category = ""
        category = ""
        
        news_dict = self.json_utility.make_json_array_for_rcmd_news(news_info_list)
        
        news_list = news_dict['news_list']
        
        for news in news_list:
            try:
                news_id = news['id']
                link = news['link']
                source = news['source']
                title = news['title']
                published_date = news['published_parsed']
                media_content = news['media_content']
                category = news['category']
                
                rcmd_news = RcmdNews.objects.create(news_id=news_id,source=source, title= title,link = link,
                                                    published_date = published_date, media_content = media_content,
                                                    news_category = category)
                rcmd_news.save()
            except KeyError as e:
                logger.error("keyError" + str(e))
                pass
        

    def getSource(self, param):
        return ""
        pass
        
        
        
        


