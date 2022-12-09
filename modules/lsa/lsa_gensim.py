# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:15:03 2020

@author: cvicentm
"""
from tqdm import tqdm
from gensim.models import LsiModel
import pickle
from gensim.models import CoherenceModel
import gc
from scipy.signal import savgol_filter
import os
#MIS IMPORTACIONES-------------------------------------

def knee_locator_coherence_u_mass(score, curve='convex', direction='decreasing'):
	"""This funtion localize where is the optimal number of clusters"""
	from kneed import KneeLocator

	x = range(1, len(score)+1)
	#son super importantes las variables curve y direction o el KneeLocator no funcionará correctaente
	kn = KneeLocator(x, score, curve=curve, direction=direction)
	
	return kn.knee

def graphic_coherence_u_mass(knee,score, start, end, step):
	"""This function print a graph score of all the validators scores"""
	import matplotlib.pyplot as plt

	x = range(start,end,step)
	plt.xlabel('Número de temas en LSA')
	plt.ylabel('Coherencia umass')
	plt.plot(x, score, 'b')
	plt.vlines(knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')


def LSA_model(generator_normalize,corpus,id2word, start = 50, step = 10, end = 80, num_words = 20):

    coherencevalueArray = []
    n_documents = len(generator_normalize)
    
    if not os.path.exists('D:\\caleb\\pickle\\'+str(n_documents)):
        os.makedirs('D:\\caleb\\pickle\\'+str(n_documents))
    
    for i in tqdm(range(start,end,step)):
    
        file_lsa_model = 'D:\\caleb\\pickle\\'+str(n_documents)+'\lsa_model_'+str(i)+'_'+str(n_documents)+'.sav'
        try:
           
            f=open(file_lsa_model, 'rb')
            lsi = pickle.load(f)
            print("The model has been trained previously with..."+str(i)+" n_topics") 
            coherencemodel = CoherenceModel(model=lsi, corpus=corpus, dictionary=id2word, coherence='u_mass')
            print("coherencia cv")
            coherencemodel_cv = CoherenceModel(model=lsi, texts=list(generator_normalize), dictionary=id2word, coherence='c_v')
            print("coherencia c_uci")
            coherencemodel_c_uci = CoherenceModel(model=lsi, texts=list(generator_normalize), dictionary=id2word, coherence='c_uci')
           
            #---------------------------------------------------------------------------------
            #SALVADO DE COHERENCIA CV Y UCI, la coherencia umass si se puede procesar en spyder
            file_cv = "D:\\caleb\\pickle\\"+str(n_documents)+"\\coherence\\cv_"+str(i)+'.txt'
            file_c_uci = "D:\\caleb\\pickle\\"+str(n_documents)+"\\coherence\\c_uci_"+str(i)+'.txt'
            pickle.dump(coherencemodel_cv, open(file_cv, 'wb'))
            pickle.dump(coherencemodel_c_uci, open(file_c_uci, 'wb'))
            #---------------------------------------------------------------------------------
            
            #CoherenceModel(model=goodLdaModel, texts=texts, dictionary=dictionary, coherence='c_v')
            #coherencemodel = CoherenceModel(model=lda, texts=list(generator_normalize), dictionary=id2word, coherence='c_v')
            coherence_values = coherencemodel.get_coherence()
            coherencevalueArray.append(coherence_values)
            
        except IOError:
            
            print("FINALLY: the LSA model has to be trained for "+str(n_documents)+" n_documents and "+str(i)+" n_topics, trained")
            lsi = LsiModel(corpus, id2word=id2word, num_topics=i)
            print("Lsi paso 2")
            #corpus_lsi = lsi[corpus]
            
            #n_words = sum( [ len(item) for item in corpus_tfidf[0:7]])
            print("coherence")
            coherencemodel = CoherenceModel(model=lsi, corpus=corpus, dictionary=id2word, coherence='u_mass')
            print("coherencia cv")
            coherencemodel_cv = CoherenceModel(model=lsi, texts=list(generator_normalize), dictionary=id2word, coherence='c_v')
            print("coherencia c_uci")
            coherencemodel_c_uci = CoherenceModel(model=lsi, texts=list(generator_normalize), dictionary=id2word, coherence='c_uci')
            
            #---------------------------------------------------------------------------------
            #SALVADO DE COHERENCIA CV Y UCI, la coherencia umass si se puede procesar en spyder
            file_cv = "D:\\caleb\\pickle\\"+str(n_documents)+"\\coherence\\cv_"+str(i)+'.txt'
            file_c_uci = "D:\\caleb\\pickle\\"+str(n_documents)+"\\coherence\\c_uci_"+str(i)+'.txt'
            pickle.dump(coherencemodel_cv, open(file_cv, 'wb'))
            pickle.dump(coherencemodel_c_uci, open(file_c_uci, 'wb'))
            #---------------------------------------------------------------------------------
    
            
            coherencevalue = coherencemodel.get_coherence()
            coherencevalueArray.append(coherencevalue)
            
            file_lsa_model = 'pickle\\'+str(len(generator_normalize))+'\lsa_model_'+str(i)+'_'+str(len(generator_normalize))+'.sav'
            pickle.dump(lsi, open(file_lsa_model, 'wb'))                  
            
        #vaciar memoria RAM
        gc.collect()
        
#-------------------------------------------------------------------------------------

    
    coherence_value = 'D:\\caleb\\pickle\\'+str(len(generator_normalize))+'\coherencevalueArray'+str(i)+'_'+str(len(generator_normalize))+'.sav'
    pickle.dump(coherencevalueArray, open(coherence_value, 'wb'))  
    #score = savgol_filter(coherencevalueArray, 11, 3)
    """
    score = coherencevalueArray
    knee=knee_locator_coherence_u_mass(score)
    best_model = int(start+knee*step)
    graphic_coherence_u_mass(best_model,score, start,end,step)
    """
    best_model = 27
    file_lsa_best_model = 'pickle\\'+str(n_documents)+'\lsa_model_'+str(best_model)+'_'+str(n_documents)+'.sav'
    f=open(file_lsa_best_model, 'rb')
    lsa = pickle.load(f)
    
    
    topics_resume = lsa.show_topics(num_topics=best_model, num_words=num_words, log=False, formatted=True)

    
    return lsi, topics_resume, best_model
