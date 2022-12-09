# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 09:34:03 2020

@author: cvicentm
"""


from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from nltk import word_tokenize
from tqdm import tqdm
from gensim.utils import simple_preprocess
import numpy as np
import pandas as pd
#---------------------------
from modules.sql import dBAdapter
from modules.pre import create_corpus as c
from modules.sql import helpers as h
from modules.lsa import tfidf

n_documents = 500

name_database = 'tfg_project'
name_collection = 'tv_storage'

max_documents= h.max_documents(name_database, name_collection)
n_documents = 50 
[dic_subtitles, generator_normalize, n_documents]=h.import_dict_and_normalize( name_database, name_collection, n_documents)



id2word = Dictionary(generator_normalize)
corpus = [id2word.doc2bow(text) for text in generator_normalize]

model = TfidfModel(corpus, smartirs='ntc')  
#vector = model[corpus[0]]  

result_day =  tfidf.more_important_words_by_day(dic_subtitles,corpus,id2word,model,'2016 11 16')



