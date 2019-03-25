from django.db import models
from pygments.lexers import get_lexer_by_name
from datetime import datetime

class RcmdNews(models.Model):
    
    def __str__(self):
        return "제목: " + self.title
    
    news_id = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=500)
    published_date = models.CharField(max_length=100)
    media_content = models.CharField(max_length=2000)
    source = models.CharField(max_length=30, default='보리뉴스')
    news_category = models.CharField(max_length=2000, default='default')
