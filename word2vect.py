# -*- coding: utf-8 -*-
"""
Created on Sun May 24 17:35:53 2020

@author: cvicentm
"""



n_documents = 200

import nltk
from nltk import word_tokenize
from tqdm import tqdm
#MIS LIBRERÍAS
from modules.pre import create_corpus as c
from modules.pre import get_data as gt
from modules.sql import helpers as h
from modules.sql import dBAdapter



name_database = 'tfg_project'
name_collection = 'tv_storage'

old_max_documents = h.max_documents(name_database,name_collection)
[list_subt_token, new_max_documents ]= h.import_doc2vec_list(name_database, name_collection, old_max_documents)


data = []
for l in list_subt_token:
    new = list(filter(None, l))
    data.append(new)

from gensim.models import Word2Vec

print("start to train model")
word2vec = Word2Vec(data, min_count=2)
print("model training finsihed")
vocabulary = word2vec.wv.vocab

index2word = word2vec.wv.index2word

word2vec.wv.save_word2vec_format('tensorr')

word2vec.wv.most_similar('Steven-Spielberg')
word2vec.wv.most_similar(positive=['mujer', 'presidente'], negative=['hombre'])

#most_similar use cosine_similarity--> Cosine_distance = 1 - cosine_similarity
#Project_embedding use cosine_distance



#python -m gensim.scripts.word2vec2tensor --input model_name --output tf_name
#ir a la página de https://projector.tensorflow.org/