# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:38:18 2020

@author: cvicentm
"""

"""IN THIS PROGRAM THE CODE DOC2VEC WILL BE EXECUTED """

from modules.doc2vec import doc2vec as d2v
from modules.classificator import k_means_doc2vec as k
from modules.sql import helpers as h
from modules.sql import dBAdapter 
#----------------------------------
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import timeit
import numpy as np
import pickle
from tqdm import tqdm
import os

database = 'tfg_project'
collection = 'tv_storage'
dbAdapter = dBAdapter.Database(database, collection)
dbAdapter.open()
max_documents = dbAdapter.get_maxDocuments()
dbAdapter.close()

max_clusters = 200
n_documents = max_documents
vector_size_array = [27, 50, 75,100, 200,300]
knee_array = []
score_array = []

for vector_size in vector_size_array:
    print("Estamos con el vector size "+ str(vector_size))
    [list_vec_doc2vec, arr_vec_doc2vec, train_data, model,dic_subtitles]=d2v.doc2vec_module(database, collection, n_documents = n_documents, vector_size = vector_size, max_clusters = max_clusters)
    
    #Para saber las palabras más parecidas con el modelo DM
    #model.wv.most_similar('cantar')
    
    score = k.validator_cluster(arr_vec_doc2vec, max_cluster=max_clusters, min_cluster=1)
    score_array.append(score)
    
    
    knee = k.knee_locator_k_means(score)
    knee_array.append(knee)
    
    k_means_optimized = KMeans(n_clusters=knee).fit(arr_vec_doc2vec)
    
    #----------------------------------------------------------------
    
    index_clusters = k.similar_subtitles(dic_subtitles,k_means_optimized,knee,k_means_optimized)
    
    subtitles = list(dic_subtitles.keys())
    
    vector_dataframe = k.vectfordoc(arr_vec_doc2vec, vector_size, subtitles, index_clusters)
    
    n_documents = len(subtitles)
    k.printClusterDf(vector_dataframe, n_documents,index_clusters,vector_size)
    
    print("printing into excel documents for days")
    df = pd.DataFrame({'A' : [np.nan]})
    days = k.list_days(dic_subtitles)
    if not os.path.exists('results\\doc2vec\\days\\'+str(n_documents)+'\\'+str(vector_size)):
            os.makedirs('results\\doc2vec\\days\\'+str(n_documents)+'\\'+str(vector_size))
    with pd.ExcelWriter('results\\doc2vec\\days\\'+str(n_documents)+'\\'+str(vector_size)+'\\day_clusters'+str(n_documents)+'.xlsx') as writer:
            df.to_excel(writer, sheet_name="main") 
    days = ['2017 08 10','2017 10 27', '2018 04 12'] 
    for day in tqdm(days):
        k.printDayDf(day, vector_dataframe, n_documents, index_clusters, dic_subtitles,k_means_optimized, knee,vector_size)




"""IMPORTANTE"""
#Poner el modelo de palabras en el Embedding Projector
#model.wv.save_word2vec_format('doc2vec_model')
#ejecutar el siguiente comando en cmd donde se encuentre la ruta de model_name
#python -m gensim.scripts.word2vec2tensor --input doc2vec_model --output tf_name
#ir a la página de https://projector.tensorflow.org/
#salen demasiadas palabras, quitar unas cuantas

"""
#-----------------------------------------------------------------------------------------------------
#COMPARATION BETWEEN K_MEANS AND PCA KMEANS
#-----------------------------------------------------------------------------------------------------
plt.figure(0)
tic=timeit.default_timer()
knee_c=d2v.doc2vec_kmeans_similarity(arr_vec_doc2vec, max_clusters)
toc=timeit.default_timer()
print("Time using normal k_means: "+str(toc-tic))
plt.figure(1)
tic=timeit.default_timer()
[components,knee_pca]=d2v.doc2vec_kmeans_pca(arr_vec_doc2vec, max_clusters)
toc=timeit.default_timer()
print("Time using PCA k_means: "+str(toc-tic))
"""
#START PCA: ------------------------------------------------------------------------------------------




"""
plt.figure(3)
plt.scatter(components[:, 2], components[:, 1], c=prediction, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 2], centers[:, 1], c='black', s=200, alpha=0.5);


score_completed=validator_cluster(arr_vec_doc2vec,100)
knee2 = k.knee_locator_k_means(score_completed)
plt.figure(4)
k.graphic_k_means_validator(knee2,score_completed)
"""



#FINISHED PCA: -------------------------------------------------------------------------