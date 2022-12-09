# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:23:51 2020

@author: cvicentm
"""
import pickle
from gensim.models import CoherenceModel
from modules.sql import dBAdapter
from modules.pre import create_corpus as c
import gensim
import gensim.corpora as corpora
from gensim.corpora.dictionary import Dictionary

n_documents = 10
n_topics = 15


"""
[generator_normalize, dic_subtitles] = c.create_corpus(n_documents)
for gn in generator_normalize:
    while True:
        try:
            gn.remove(None)
        except ValueError:
            break
        
dictionary = Dictionary(generator_normalize)
print("Getting body subtitles from the database finished ...")
id2word = corpora.Dictionary(generator_normalize)
corpus = [id2word.doc2bow(text) for text in generator_normalize]
print("empezando con el lda")

lda = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=n_topics, 
                                               random_state=100,
                                               update_every=1,
                                               chunksize=100,
                                               passes=10,
                                               alpha='auto',
                                               per_word_topics=True)

goodLdaModel = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, iterations=50, num_topics=n_topics)
print("empezando con la coherencia")

goodcm = CoherenceModel(model=goodLdaModel, texts=generator_normalize, dictionary=dictionary, coherence='c_v')
coherence_values = goodcm.get_coherence()
print(coherence_values)
"""

texts = [['human', 'interface', 'computer'],
         ['survey', 'user', 'computer', 'system', 'response', 'time'],
         ['eps', 'user', 'interface', 'system'],
         ['system', 'human', 'system', 'eps'],
         ['user', 'response', 'time'],
         ['trees'],
         ['graph', 'trees'],
         ['graph', 'minors', 'trees'],
         ['graph', 'minors', 'survey']]
dictionary = Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]   
print("lda")
goodLdaModel = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, iterations=50, num_topics=2)
print("coherence model")
goodcm = CoherenceModel(model=goodLdaModel, texts=texts, dictionary=dictionary, coherence='c_v')
print("get_coherence")
coherence = goodcm.get_coherence()



