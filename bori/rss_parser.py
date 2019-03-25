import feedparser
import urllib.request
from bs4 import BeautifulSoup

import logging
import sys
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class rss_parser():
    
    def __init__(self):
        #self.header = 'http://news.google.co.kr/news?hl=ko&ned=kr&ie=UTF-8&q='
        self.header = 'https://news.google.com/news/rss/search/section/q/'
        #self.tail = '&output=rss'
        self.tail = '?hl=ko&gl=KR&ned=kr'
        
        
    
    def encode_objective_word(self,word):
        endcoded_word = urllib.parse.quote(word.encode('utf8'))
        
        return endcoded_word
        
    def parse_feed_with_word(self,word):
        #d = feedparser.parse('http://news.google.co.kr/news?hl=ko&ned=kr&ie=UTF-8&q=%EC%86%8C%EC%84%A4&output=rss')
        word = self.encode_objective_word(word)
        url = self.header + word + self.tail
        news = feedparser.parse(url)
        return news
     
    def parse_feed_with_url(self,url):
        news = feedparser.parse(url)
        return news
    
    def get_img_src(self,summary):
        try:
            soup = BeautifulSoup(summary,'html5lib')
            #img_src = soup.find('img').get('src')
            img_src = soup.find('img')['src']
        except:
            logger.debug('No Img src')
            img_src = ''
        
        return img_src
    
    def get_news_info(self,news, category):
        start_time = time.time()
        
        post_list = []
        
        
        for post in news.entries:

            
            post['category'] = category
            
            #logger.info('post type: ' + str(type(post)))
         
            '''
            try:
                id = post['id']
                #logger.debug('Post id:%s', id)
                
            except Exception as e:
                logger.debug('Fail to get id: ' + str(e))
                continue

            summary = post['summary']
            img_src = self.get_img_src(summary)
           
            title = post['title']
            link = post['link']
            
            logger.debug('Post title:%s', title)
          
            news_dict = {'id':id, 'title':title, 'link':link, 'img_src': img_src}
            '''
            post_list.append(post)
            
        logger.debug('Getting news post time:%f', time.time() - start_time)
        
        return post_list

