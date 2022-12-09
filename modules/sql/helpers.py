# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 19:17:57 2020

@author: cvicentm
"""
from modules.pre import create_corpus as c
from modules.pre import get_data as g
from modules.sql import dBAdapter

def mongo_q_to_dict(mongo_q):
    "Esta funcion convierte una consulta de python en un diccionario"
    result = {}
    for mq in mongo_q:
        result[mq['name']]=mq['subtitle']
    return result

def mongo_q_doc2vec_to_list(mongo_q_doc2vec):
    result = []
    for mq in mongo_q_doc2vec:
        result.append(mq['doc2vec'])
    return result
def mongo_q_generator_normalize_to_list(mongo_q_normalize):
    result = []
    for mq in list(mongo_q_normalize):
        result.append(mq['normalize'])
    return result

def import_dict_and_normalize(name_database,name_collection,n_documents):
    print("Getting body subtitles from the database started ...")
    dbAdapter= dBAdapter.Database(name_database,name_collection)
    dbAdapter.open()
    listado=dbAdapter.selectGenerator_normalize_limit(n_documents)
    dic_subtitles = dbAdapter.selectDic_subtitles_limit(n_documents)
    dbAdapter.close()
    print("finalizada consulta")
    
    dic_subtitles2 = dic_subtitles
    
    generator_normalize = []
    for i in range(len(listado)):
        try:
            generator_normalize.append(listado[i].split(","))
        except:
            dic_subtitles2.pop(list(dic_subtitles.keys())[i])
            print("generator NonType------>"+str(i))
    
    dic_subtitles = dic_subtitles2
            
    for gn in generator_normalize:
        while True:
            try:
                gn.remove("")
            except ValueError:
                break
    print("Getting body subtitles from the database finished ...")
    n_documents = len(generator_normalize)
    
    return dic_subtitles, generator_normalize, n_documents

def import_doc2vec_list(name_database, name_collection,n_documents):
    dbAdapter = dBAdapter.Database(name_database, name_collection)
    dbAdapter.open()
    print("Getting doc2vec list started...")
    list_s=dbAdapter.select_dataDoc2Vec(n_documents)
    print("Getting doc2vec list finished...")
    dbAdapter.close()
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
    
    return data, n_documents

def max_documents(name_database,name_collection):
    dbAdapter= dBAdapter.Database(name_database, name_collection)
    dbAdapter.open()
    max_documents = dbAdapter.get_maxDocuments();
    dbAdapter.close()
    return max_documents

def update_doc2vec():
    #------------------------------------------------------
    #UPDATE DDBB DOC2VEC
    #------------------------------------------------------
    [files, max_documents] = g.get_NameFiles()
    [dic_subtitles,data]=c.create_d2v_corpus(max_documents)
    subtitles=list(dic_subtitles.keys())
    data_s=[]
    for d in data:
        data_s.append(','.join(d))
    print("updating the database")
    dbAdapter = dBAdapter.Database('tfg_project','tv_storage')
    dbAdapter.open()
    for i in range(len(data_s)):
        dbAdapter.update_doc2vec(subtitles[i],data_s[i])
    dbAdapter.close()