# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:24:12 2020

@author: cvicentm
"""
import gensim
from random import randint
import pandas as pd
import os
from tqdm import tqdm
import numpy as np
from sklearn.cluster import KMeans
#start my modules importation ----------------------------
from modules.pre import get_data as g
from modules.pre import create_corpus as c
from modules.classificator import k_means_classificator as kmc
from modules.lda.unsupervised_learning_gensim import LDAmodel
from modules.lda.unsupervised_learning_gensim import printColorWordDocument
import modules.variables as v
from itertools import chain
import matplotlib.pyplot as plt


channels = v.CHANNELS
#end my modules importation ------------------------------

#importar csv para visualizar en power bi------------------------------
def results2csv():
    #resumen completo de tópicos por subtitulo-------------------------
    list_channels = []
    days = []
    for subtitle in list(dic_subtitles.keys()):
        list_channels.append(c.get_channel(subtitle)[0])
        days.append(c.get_date(subtitle))
    years = []
    for day in days:
        years.append(day[:4])
        
    dfpbi = topic_dataframe.T
    
    dfpbi = topic_dataframe.T.reset_index()
    
    dfpbi.insert(len(dfpbi.columns),"channel",list_channels)
    dfpbi.insert(len(dfpbi.columns),"day",days)
    dfpbi.insert(len(dfpbi.columns),"year",years)
    dfpbi.to_csv("data\\df.csv")
    
    #media de tópicos por cadena y por año------------------------------
    channels = v.CHANNELS

    topics = []
    for i in range(best_n_topic):
        topics.append('Topic_'+str(i+1))
    
    suma = dfpbi[topics].astype(float)
    suma.insert(suma.shape[1],'channel',dfpbi['channel'])
    suma.insert(suma.shape[1],'year',dfpbi['year'])
    suma = suma.groupby(['channel','year']).mean()
    suma = suma.reset_index()
    suma.to_csv("data\\df_topics_per_channel.csv")
    
    """   
    topics_per_channel = np.zeros((len(channels),len(topics)))
        
    for i in range(len(channels)):
        for j in range(len(topics)):
            topics_per_channel[i][j] = dfpbi.loc[dfpbi['channel']==channels[i]][topics[j]].astype(float).sum(axis=0)/len(dfpbi.loc[dfpbi['channel']==channels[i]])
        
    dataframe = pd.DataFrame(topics_per_channel.T, dtype="str", index=topics).T
    dataframe.insert(dataframe.shape[1],'channel',channels)
    """

#resumen de topicos----------------------------------------------------
"""IN THIS CODE WE WILL EXECUTE THE CODE RELATED TO LDA"""

start_topics = 1
N_TOPICS = 2
step = 2

#este parámetro no se puede añadir a mano
n_printedDocuments =20
max_clusters= 200


from modules.sql import dBAdapter
name_database = 'tfg_project'
name_collection = 'tv_storage'
dbAdapter= dBAdapter.Database(name_database, name_collection)
dbAdapter.open()
max_documents = dbAdapter.get_maxDocuments();
dbAdapter.close()

#if we want to change the number of documents to analized we can do it here
n_documents=max_documents

#PROGRAM-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[array_topic_per_document, best_n_topic, dic_subtitles,lda,generator_normalize,corpus,id2word,coherencemodelArray,perplexitymodelArray,boundArray]=LDAmodel(N_TOPICS,n_documents, n_printedDocuments,name_database,name_collection, step,start=start_topics)

best_n_topic = 27

#CUIDADO CON ESTO
n_documents = len(generator_normalize)

score = kmc.validator_cluster(array_topic_per_document, max_cluster=max_clusters, min_cluster=1)

knee = kmc.knee_locator_k_means(score)

kmc.graphic_k_means_validator(knee,score)

k_means_optimized = KMeans(n_clusters=knee).fit(array_topic_per_document)

kmc.showGraphsLDATrainedInTerminal(dic_subtitles, array_topic_per_document, best_n_topic, 5)

index_clusters = kmc.similar_subtitles(dic_subtitles,k_means_optimized,knee,k_means_optimized)

kmc.printClusters2Document(index_clusters,n_documents,dic_subtitles)

#print report about main parameters of the analysis
kmc.printResults2Document(max_documents, n_documents, dic_subtitles, N_TOPICS, best_n_topic, max_clusters, knee, id2word)

topic_dataframe = kmc.topic_per_document_pandas(array_topic_per_document, best_n_topic, dic_subtitles, index_clusters)

kmc.printClusterDf(topic_dataframe, n_documents,index_clusters)

topics_resume = lda.show_topics(num_topics=28, num_words=int(len(list(dict(id2word).keys()))), log=False, formatted=True)

#resultados in csv to use them into power bi
results2csv()
#ORDENAR UN POCO ESTE CÓDIGO
#printing into an excel all the topics of the days



print("printing into excel documents for days")
df = pd.DataFrame({'A' : [np.nan]})
days = kmc.list_days(dic_subtitles)
if not os.path.exists('results\\days\\'+str(n_documents)):
        os.makedirs('results\\days\\'+str(n_documents))
with pd.ExcelWriter('results\\days\\'+str(n_documents)+'\\day_clusters'+str(n_documents)+'.xlsx') as writer:
        df.to_excel(writer, sheet_name="main") 
for day in tqdm(days[0:20]):
    kmc.printDayDf('2017 10 27', topic_dataframe, n_documents, index_clusters, dic_subtitles,k_means_optimized, knee)


#PRUEBAS---------------------------------------------------------------------------------------------------


#IMPRIMIR DOCUMENTOS DE WORD--------------------------------------------------------------
#MEDIR LA PERPLEJIDAD DEL MODELO:
#lda_model.log_perplexity(corpus)
"""
print("ha llegado a entrenar el modelo")
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=best_n_topic, 
                                               random_state=100,
                                               update_every=1,
                                               chunksize=100,
                                               passes=10,
                                               alpha='auto',
                                               per_word_topics=True)



colors = []

print("ha llegado hasta la parte de los colores")   

for i in range(best_n_topic):
    colors.append('#%06X' % randint(0, 0xFFFFFF))
colors.append('#000000')
#creation of the directory which content all documents printed
if not os.path.exists('word\\'+str(n_documents)):
        os.makedirs('word\\'+str(n_documents))
      
print("colour´s documented are being printed")

subtitles = list(dic_subtitles.keys())
day_subtitles = [subtitles.index(item) for item in subtitles if '2018 12 25' in item]
for i in tqdm(day_subtitles):
    printColorWordDocument(i,colors,generator_normalize,dic_subtitles,lda_model,corpus,n_documents)

print("el mejor tópicoooooooooooo:"+str(best_n_topic))
#------------------------------------------------------------------

lines = []
labels = [subtitles[item] for item in day_subtitles]
x = list(range(1,best_n_topic+1))
f = plt.figure(figsize=(50,10))
ax = f.add_subplot(121)
#n_topics+1 because has to have the same weight than coherencemodelArray
#score = savgol_filter(coherencemodelArray, 11, 3)
for i in day_subtitles:
    ax.plot(x, array_topic_per_document[i])
    ax.legend(labels)
ax.xlabel("Temas")
ax.ylabel("Porcentaje")
ax.show()


"""

