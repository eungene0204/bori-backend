import os
from gensim.models import Word2Vec

class Word2VecModelReader():
    
    def __init__(self):
        self.module_dir = os.path.dirname(__file__)
        self.model_name = os.path.join(self.module_dir,'data','word2vec_model_noun_20171013')

    def load_model(self):
        model = Word2Vec.load(self.model_name)
        num_feature = 300

        return model, num_feature

