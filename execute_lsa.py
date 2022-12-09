# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:13:04 2020

@author: cvicentm
"""

from gensim.models import TfidfModel
from gensim.models import hdpmodel
from gensim.corpora import Dictionary
from nltk import word_tokenize
from tqdm import tqdm
from gensim.utils import simple_preprocess
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

#---------------------------
from modules.sql import dBAdapter
from modules.pre import create_corpus as c
from modules.sql import helpers as h
from modules.lsa import tfidf
from modules.lsa import lsa_gensim

#START FUNCTIONS-------------------------------------------------------------------------

name_database = 'tfg_project'
name_collection = 'tv_storage'

max_documents= h.max_documents(name_database, name_collection)
n_documents = max_documents
[dic_subtitles, generator_normalize, n_documents]=h.import_dict_and_normalize( name_database, name_collection, n_documents)


id2word = Dictionary(generator_normalize)
corpus = [id2word.doc2bow(text) for text in generator_normalize]
#poniendo el parametro rm a 1 se aplica la eliminación del 50% de cada documento del corpus
[corpus_tfidf,model] = tfidf.train_tfidf(corpus, rm = 0)

start = 27
end = 28
step = 1

"""Recordar que LSA no está suavizando la curva de de la coherencia"""
[lsa, topic_resume, best_model]= lsa_gensim.LSA_model(generator_normalize,corpus_tfidf,id2word,start, step, end, num_words = 20)

#ANALISIS DEL TFIDF POR DIA
result_day =  tfidf.more_important_words_by_day(dic_subtitles,corpus,id2word,model,'2017 10 27')






"""
Hdp_model = hdpmodel.HdpModel(corpus=corpus, id2word=id2word)
topics_resume_hdp = Hdp_model.print_topics(num_topics=70, num_words=10)
----------------------------------------------------------------------
"""

"""
#DEMOSTRACIÓN QUE EN LSA LOS TÓPICOS SE COMPARAN ENTRE DOCUMENTOS Y NO SE COGEN DE UN SOLO DOCUMENTO
#se ha demostrado porque para un tópico contiene(aunque con muy poco probabilidad) mas palabras que cualquier documento
#para este entrenamiento: lsi = LsiModel(corpus_tfidf[0:7], id2word=id2word, num_topics=i)
cpl = list(cp)

gnl = generator_normalize[0:7]

a = topics_resume1[0][]

a = topics_resume1[0][1]

string = a.split(" + ")

lista = [s.split("*") for s in string]

df = pd.DataFrame(lista)
"""




