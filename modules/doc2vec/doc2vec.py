# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:03:26 2020

@author: cvicentm
"""

import gensim
from tqdm import tqdm
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import os
import configparser
import ast
import matplotlib.pyplot as plt
from tqdm import tqdm


#start my importations------------------------
"""
import sys
sys.path.insert(0,'..')
"""
from modules.sql.dBAdapter import Database
from modules.pre import create_corpus as c
from modules.classificator import k_means_doc2vec as km_d2v
from modules.pre import get_data as g
from modules.sql import dBAdapter

#end my importations--------------------------
config = configparser.ConfigParser()
config.read('config\\config.ini')


#start config variables---------------------------------------------------------------------

def doc2vec_module(database, collection, n_documents = 300, vector_size = 50, max_clusters = 200):
    
    
    
    #logs
    file_logs = config['LOGS']['doc2vec_logs']
    name_log_file = datetime.now().strftime(file_logs+'_%d_%m_%Y.log') 
    logging.basicConfig(filename=name_log_file, level=logging.WARNING, 
                        format="%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s") 
    
    #end config variables-----------------------------------------------------------------------
        
    
    #import from DDBB dic_subtitles and data doc2vec --------------------------
    print("Getting body subtitles from the database started ...")
    data=[]
    dbAdapter = dBAdapter.Database( database, collection)
    dbAdapter.open()
    dic_subtitles = dbAdapter.selectDic_subtitles_limit(n_documents)
    subtitles=list(dic_subtitles.keys())
    list_s=dbAdapter.select_dataDoc2Vec(n_documents)
    print("Getting body subtitles from the database finished ...")
    data=[]
    for l in list_s:
        data.append(l.split(","))
    for d in data:
        while True:
            try:
                d.remove("")
                d.remove(" ")
            except ValueError:
                break
    
    
    #--------------------------------------------------------------------------
    
    # Create the tagged document needed for Doc2Vec
    def create_tagged_document(list_of_list_of_words):
        for i, list_of_words in enumerate(list_of_list_of_words):
            yield gensim.models.doc2vec.TaggedDocument(list_of_words, [subtitles[i]])
    
    train_data = list(create_tagged_document(data))
    
    print("starting with doc2vec....")
    model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=2, epochs=40)
    
    # Build the Volabulary
    model.build_vocab(train_data)
    
    # Train the Doc2Vec model
    model.train(train_data, total_examples=model.corpus_count, epochs=model.epochs)
    
    list_vec_doc2vec = [model.docvecs[subtitle] for subtitle in subtitles]
    
    arr_vec_doc2vec = np.stack( list_vec_doc2vec, axis=0 )
    
    
    return list_vec_doc2vec, arr_vec_doc2vec, train_data, model, dic_subtitles

def doc2vec_kmeans_similarity(arr_vec_doc2vec, max_clusters):
    #K_MEANS SIMILARITY: -------------------------------------------------------------------------
    knee=0
    try:
        score = km_d2v.validator_cluster(arr_vec_doc2vec, max_clusters ,min_cluster=1)
        try:
            knee = km_d2v.knee_locator_k_means(score)
            #plt.figure(1)
            km_d2v.graphic_k_means_validator(knee,score)
        except:
            logging.warning("Kmeans doc2vec error score has not been fill completely.")
    except ValueError:
        
        logging.warning("Value error: n_clusters should be less than documents we are using")   
    
    return knee
        
    #k_means_optimized = KMeans(n_clusters=knee).fit(arr_vec_doc2vec)

def doc2vec_kmeans_pca(arr_vec_doc2vec, max_clusters):  
    #K_MEANS PCA: -------------------------------------------------------------------------
    #k_means with PCA
    [components, vr, knee] = km_d2v.pca_doc2vec(arr_vec_doc2vec)
    plt.figure(1)
    km_d2v.graphic_k_means_validator(knee,vr)
    
    score=km_d2v.validator_cluster(components[:,0:knee],max_clusters)
    knee = km_d2v.knee_locator_k_means(score)
    plt.figure(2)
    km_d2v.graphic_k_means_validator(knee,score)
    
    """
    kmeans = KMeans(n_clusters=knee)
    kmeans.fit(components[:,0:knee])
    prediction = kmeans.predict(components[:,0:3])
    """
    
    return components, knee
    
def d2v_kmeans2excel(arr_vec_doc2vec, dic_subtitles,n_documents,knee):
    #RESULTS K_MEANS DOC2VEC TO EXCEL---------------------------------------------------------------
    subtitles = list(dic_subtitles.keys())
    k_means_optimized = KMeans(n_clusters=knee).fit(arr_vec_doc2vec)
    
    index_clusters = km_d2v.similar_subtitles(dic_subtitles,k_means_optimized,knee, k_means_optimized)
           
    vec_dataframe = km_d2v.vectfordoc(arr_vec_doc2vec, np.shape(arr_vec_doc2vec)[1], subtitles, index_clusters)
    
    km_d2v.printClusterDf(vec_dataframe, n_documents,index_clusters)
    #ORDENAR UN POCO ESTE CÓDIGO
    #printing into an excel all the topics of the days
    path_days = config['DOC2VEC']['path_results_days']
    print("printing into excel documents for days")
    df = pd.DataFrame({'A' : [np.nan]})
    days=km_d2v.list_days(subtitles)
    if not os.path.exists(path_days+str(n_documents)):
            os.makedirs(path_days+str(n_documents))
    with pd.ExcelWriter(path_days+str(n_documents)+'\\day_clusters'+str(n_documents)+'.xlsx') as writer:
            df.to_excel(writer, sheet_name="main") 
    for day in tqdm(days[0:10]):
        km_d2v.printDayDf(day, vec_dataframe, n_documents, index_clusters, subtitles,k_means_optimized, knee)

