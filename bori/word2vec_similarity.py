import sys
sys.path.insert(0,'../calculation')
import pandas as pd
import re
from konlpy.tag import Twitter; t = Twitter()
from collections import defaultdict
import numpy as np
from .numpy_util import numpy_util

#np.seterr(divide='ignore',invalid='ignore')


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class word2vec_similarity():
    def __init__(self,model,num_features):
        #self.samples = pd.read_csv('../data/twt_test_samples.csv', header = 0, quoting=3, encoding='cp949',
        #                            error_bad_lines=False)
        #self.sample_value = self.samples.values
        self.num_features = num_features
        self.model = model
        self.np_util = numpy_util()
        

    def get_clean_tweet(self,samples):
        clean_twt = []
        for twt in samples:
            tweet = twt[0]
            category = twt[1]
            if(isinstance(tweet,str)):
                hangul = re.findall(u'[\uAC00-\uD7A3]+', tweet)
                hangul = t.morphs(' '.join(hangul))
                clean_twt.append([hangul,category])
        return clean_twt
   
    def makeFeatureVec(self, twts):
        vec_list =[]
        featureVec = np.zeros((self.num_features,), dtype='float32')
        nwords = 0
        index2word_set = set(self.model.index2word)
    
        # check if it is in the model's vocabulary
        twt = twts[0]
        category = twts[1]
        logger.debug('Twt in word2vec sim:%s', twt)
        logger.debug('category in word2vec sim:%s', category)
        for word in twt:
            if word in index2word_set:
                nwords = nwords + 1
                featureVec = np.add(featureVec, self.model[word])
           
        if(nwords > 0):
            try:
                logger.debug('featureVec:')
                featureVec = np.divide(featureVec, nwords)
            except Exception as e:
                print(e)
            vec_list.append([featureVec,category])
			
        return vec_list


    def get_avg_vector(self,sentence):
        
        if(len(sentence) <= 0):
            return
            
        avg_vector = np.zeros((self.num_features,), dtype='float32')
        nwords = 0
        index2word_set = set(self.model.index2word)
        
        for word in sentence:
            if word in index2word_set:
                nwords = nwords + 1
                avg_vector = np.add(avg_vector,self.model[word])
        
        try:
            avg_vector = np.divide(avg_vector, nwords)
        except Exception as e:
            print(e)
        
        return avg_vector
        

    def getAvgFeatureVecs(self, clean_twts):
        counter = 0
        featueVecs_list = []

        for twt in clean_twts:
            if counter % 1000 == 0.:
                print('Tweet %d of %d ' % (counter, len(clean_twts)))
            raw_twt = twt
            counter += 1
            avg_vecs_list = self.makeFeatureVec(twt)
            
            if(0 < len(avg_vecs_list)):
                avg_vec = avg_vecs_list[0]
                avgFeatureVecs = avg_vec[0]
                category = avg_vec[1]
                featueVecs_list.append([raw_twt, avgFeatureVecs, category])

        return featueVecs_list
    

    def find_most_similar_category(self,avg_vector,objective_words):
        temp_word_list=[]
        
        for word in objective_words:
            try:
                similarity = self.np_util.get_cosine_similarity(avg_vector, self.model[word])
                temp_word_list.append([similarity,word])
            except Exception as e:
                print('Exception %s' % e)
                pass
                
        sorted_list = sorted(temp_word_list,reverse=True)
        top_word = sorted_list[0]
         
        similarity = top_word[0]
        category = top_word[1]
        
        return similarity,category
       
    def get_negative_words(self):
        neg_words = pd.read_csv('../data/negative_words.csv', header = 0, quoting=3, encoding='cp949',
                                    error_bad_lines=False)
        values = neg_words.values
        return values
       
        
    def get_negative_word_vector(self,model):
        featureVec = np.zeros((self.num_features,), dtype='float32')
        nwords = 0
       
        values = self.get_negative_words()
       
        negative_words =[]
        for word in values:
            negative_words.append(word[0])
         
        for word in negative_words:
            featureVec = np.add(featureVec, model[word])
            nwords = nwords + 1
            
        featureVec = np.divide(featureVec, nwords)
        
        return featureVec
     
    def get_positive_words(self):
        pos_words = pd.read_csv('../data/positive_words.csv', header = 0, quoting=3, encoding='cp949',
                                    error_bad_lines=False)
        values = pos_words.values
        
        return values
       
        
    def get_positive_word_vector(self,model):
        featureVec = np.zeros((self.num_features,), dtype='float32')
        nwords = 0
      
        values = self.get_positive_words()
       
        positive_words=[]
        for word in values:
            positive_words.append(word[0])
         
        for word in positive_words:
            featureVec = np.add(featureVec, model[word])
            nwords = nwords + 1
            
        featureVec = np.divide(featureVec, nwords)
        
        return featureVec
   
    #DO NOT USE THIS
    def change_category_name(self, top_category):
        if(top_category=='짜장' or top_category=='짬뽕' or top_category=='탕슈육' or top_category=='탕수육'
                or top_category=='짜장면' or top_category=='간짜장' or top_category =='짜장면'):
           top_category = '중식'
            
        if(top_category=='치맥'):
            top_category='치킨'
            
        if(top_category == '꼬치'):
            top_category = '양꼬치'
            
        if(top_category == '아메리카노' or top_category== '커피'):
            top_category = '카페'
            
        if(top_category =='라자냐'):
            top_category = '파스타'
            
        neg_word = self.get_negative_words()
        
        if top_category in neg_word:
            top_category = '비추'
            
        return top_category
    
      
    def make_objective_sentence(self,sentence,most_sim_category):
        positive_words  = self.get_positive_words()
        index2word_set = set(self.model.index2word)
        objective_setence = []
        
        for word in sentence:
            if word in positive_words and word in index2word_set:
                objective_setence.append(word)
                
        return objective_setence
    
    
    def cal_distance(self,sentece_info,objective_words):
        
        if(len(sentece_info) <= 0):
            return
        
        
        hit_counter = 0
        raw_twt_list = []
        category_list = []
        predict_category_list = []
        distance_list = []
        size = len(sentece_info)
        
        
        pos_vec = self.get_positive_word_vector(self.model)
        neg_vec = self.get_negative_word_vector(self.model)
        
        for raw_twt, given_vector, category in sentece_info:
            try:
                most_similarity, most_sim_category =\
                    self.find_most_similar_category(given_vector,objective_words)

                #most_category_plus_pos_vec = self.get_avg_from_two_vectors(pos_vec,model[most_category])
                #most_category_minus_neg_vec = self.subtract_two_vectors(most_category_plus_pos_vec, neg_vec)
                

                #objective_vector = self.np_util.add_two_vectors(pos_vec, self.model[most_sim_category])
                
                
                #objective_vector = self.np_util.subtract_two_vectors(objective_vector, neg_vec)
                #distance = self.np_util.get_cosine_similarity(given_vector, objective_vector)

                distance = self.np_util.get_cosine_similarity(given_vector,self.model[most_sim_category])

                most_sim_category = self.change_category_name(most_sim_category)
               
                 
                if(distance< 0.300):
                    most_sim_category = '비추'
                    
                raw_text = raw_twt[0]
                raw_text = ' '.join(raw_text)
                         
                distance_list.append(distance)
                raw_twt_list.append(raw_text)
                category_list.append(category)
                predict_category_list.append(most_sim_category)
               
                if category == most_sim_category:
                    hit_counter += 1
               
            except Exception as e:
                print(e)
 
        print('Accuracy:')
        print(float(hit_counter/size))
       
        self.make_result_csv(distance_list, raw_twt_list,category_list,predict_category_list)
        
    def make_result_csv(self,distance_list, raw_twt_list,category_list,predict_category_list):
        
        output = pd.DataFrame(data={'distance':distance_list ,'tweets': raw_twt_list,'real_category':category_list,
                                            'predic_category':predict_category_list})

        output.to_csv('word2vec_distance_test.csv', index=False, quoting=3)
        
        
    def get_result(self,objective_words):
        clean_twt = self.get_clean_tweet(self.sample_value)
        avg_vecs = self.getAvgFeatureVecs(clean_twt)
        self.cal_distance(avg_vecs, objective_words)
        

