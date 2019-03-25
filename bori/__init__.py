from __future__ import absolute_import
from celery import app as celery_app
from .word2vec_model import word2vec_model_reader


__all__ = ['celery_app']

print('init!!!!!!!!!!!!!!!!!')
word2vec_model_reader = word2vec_model_reader.Word2VecModelReader()
word2vec_model, word2vec_num_feature = word2vec_model_reader.load_model()
