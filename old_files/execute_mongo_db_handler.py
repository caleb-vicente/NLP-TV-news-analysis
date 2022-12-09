# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 18:25:36 2020

@author: cvicentm
"""

# pip install pymongo
from pymongo import MongoClient
from modules.sql import dBAdapter
import pandas as pd
import json
from tqdm import tqdm
import logging

from modules.sql import dBAdapter

dbAdapter = dBAdapter.Database('tfg_project','tv_storage')
dbAdapter.open()
result = list(dbAdapter.selectDict())
result2 = dbAdapter.get_maxDocuments()
result3 = list(dbAdapter.selectRowByName('antena3_2019 09 14_morning_new'))
result4 = list(dbAdapter.selectDic_subtitles_limit(10))
result5 = list(dbAdapter.select_dataDoc2Vec(40))
dbAdapter.update_doc2vec("1_spa_2019 07 21_morning_new",'hola')
dbAdapter.close()

def mongo_q_doc2vec_to_list(mongo_q_doc2vec):
    result = []
    for mq in mongo_q_doc2vec:
        result.append(mq['doc2vec'])
    return result
list5=mongo_q_doc2vec_to_list(result5)
def mongo_q_to_dict(mongo_q):
    result = {}
    for mq in mongo_q:
        result[mq['name']]=mq['subtitle']
    return result
    
dict4 = mongo_q_to_dict(result4)

"""
#PRUEBAS CONSULTAS
name = "antena3_2019 09 14_morning_new"
value = "jeje"

client = MongoClient('192.168.1.39', 27017)
database = client['tfg_project']
collection = database['tv_storage']

collection.update_one({"name": name},{"$set":{"doc2vec":value}})
"""



#IMPORTAR DATA DE MYSQL TO MONGO DB
"""
print("Getting body subtitles from the database started ...")
dbAdapter= dBAdapter.Database()
dbAdapter.open()
max_documents = int(dbAdapter.get_maxDocuments()[0][0]);
n_documents=max_documents
#dic_subtitles = pd.DataFrame(dbAdapter.selectAll(n_documents))
dic_subtitles = dbAdapter.selectAll(n_documents)
dbAdapter.close()
print("finalizada consulta")


client = MongoClient('192.168.1.39',27017)
database = client['tfg_project']
collection = database['tv_storage']
for i in tqdm(range(0,n_documents,10)):
    maxi = i+10
    if maxi < n_documents:
        df = pd.DataFrame(dic_subtitles[i:maxi])
    else:
        df = pd.DataFrame(dic_subtitles[i:n_documents])


    df.columns = ['Index', 'name', 'day', 'state','timestamp', 'subtitle', 'normalize', 'doc2vec', 'channel']
    df['timestamp'] = df.timestamp.astype(str)
    #dic_subtitles.columns = [ 'name', 'day', 'state','body']
    #mydict = { "name": "John", "address": "Highway 37" }
    #x = mycol.insert_one(mydict)
    records = json.loads(df.T.to_json()).values()
    collection.insert(records)
    #GET AL COLLECTION
    #pcollection=pd.DataFrame(mycol.find( {} ))
"""