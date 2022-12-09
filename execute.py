# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 08:04:32 2020

@author: cvicentm
"""


from modules import sql

database = 'tfg_project'
collection = 'tv_storage'
dbAdapter = sql.dBAdapter.Database(database, collection)
dbAdapter.open()
max_documents = dbAdapter.get_maxDocuments()
result_mongo = list(dbAdapter.selectAll(10))
dbAdapter.close()

import mysql.connector
connection = mysql.connector.connect(host= '192.168.1.39',
                                         database= 'news_storage',
                                         user='root',
                                         password='tfg_project')
#Importar a la base de datos de subtitles
for item in result_mongo:
    name = item['name']
    channel = item['channel']
    date = item['day']
    state = item['state']
    sql = "INSERT INTO subtitles (name,channel,datee,state) VALUES ("+name+", "+channel+", "+date+" ,"+state+");"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    






"""
from nltk import word_tokenize
def get_word_dict(word):
    n=word.find("/")
    if n != -1:
        return word[0:n]
    else:
        return word
f=open("config\\es_ANY.txt","r",encoding='utf-8')
file=f.read()
dic=word_tokenize(str(file))
es_dict = [get_word_dict(word) for word in dic]
f.close()

"""
#lista=list(file)
#lista2=[item for item in lista if str(item).isnumeric()==False]
#import pandas as pd
#data = pd.read_csv("config\\es_ANY.dic.txt", sep=" ", header=None)
"""
#------------------------------------------------------
#INSERTAR DDBB DICCTIONARY Y GENERATOR NORMALIZE tv_storage
#------------------------------------------------------
from modules.pre import get_data as g
from modules.pre import create_corpus as c
[files, max_documents] = g.get_NameFiles()

[generator_normalize, dic_subtitles]=c.create_corpus(max_documents)
subtitles=list(dic_subtitles.keys())

def removing_none_words(word):
    if word != None:
        return word

gn=[]
for d in generator_normalize:
    gn.append(','.join(list(filter(removing_none_words,d))))

from modules.sql import dBAdapter
from modules.pre import create_corpus as c
dbAdapter= dBAdapter.Database()
dbAdapter.open()
for i in range(len(subtitles)):
    dbAdapter.update_body(subtitles[i],dic_subtitles[subtitles[i]])
    dbAdapter.update_generator(subtitles[i],gn[i])
dbAdapter.close()
dbAdapter= dBAdapter.Database()
dbAdapter.open()
"""

"""
#------------------------------------------------------
#INSERTAR DDBB DOC2VEC prueba
#------------------------------------------------------
from modules.pre import create_corpus as c
from modules.pre import get_data as g
[files, max_documents] = g.get_NameFiles()
[dic_subtitles,data]=c.create_d2v_corpus(max_documents)
subtitles=list(dic_subtitles.keys())
data_s=[]
for d in data:
    data_s.append(','.join(d))

from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
for i in range(len(data)):
    dbAdapter.insert_dataDoc2Vec(subtitles[i],data[i])
dbAdapter.close()
"""
"""

"""
"""
#------------------------------------------------------
#IMPORT database to json
#------------------------------------------------------
from modules.sql import dBAdapter
import json
import collections
import configparser
config = configparser.ConfigParser()
config.read('config\\config.ini')

dbAdapter= dBAdapter.Database()
dbAdapter.open()
max_documents = int(dbAdapter.get_maxDocuments()[0][0]);
tv_storage = dbAdapter.selectAll(max_documents)
dbAdapter.close()

tv_json = []
for new in tv_storage:
    d = collections.OrderedDict()
    d['id'] = new[0]
    d['name'] = new[1]
    d['date'] = new[2]
    d['state'] = new[3]
    d['autotimestamp'] = str(new[4])
    d['body'] = new[5]
    d['normalize_text'] = new[6]
    d['data_doc2vec'] = new[7]
    d['channel'] = new[8]
    tv_json.append(d)


j = json.dumps(tv_json,indent=1, ensure_ascii=False)
tv_storage_file = config['DATA']['path_tv_storage']
with open(tv_storage_file, 'w', encoding='utf8') as f:
    f.write(j)
    f.close()


"""

"""
#------------------------------------------------------
#GET DDBB update channels into database
#------------------------------------------------------
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
dic_subtitles = dict(dbAdapter.selectDict())
dbAdapter.close()
print("finalizada consulta")

import modules.variables as v
channels = v.CHANNELS

channel_column = [(subtitle, channel) for subtitle in list(dic_subtitles.keys()) 
                    for channel in channels if subtitle.find(channel)!=-1 ]

print("vamos a usar la base de datos")
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
from tqdm import tqdm
for ch in tqdm(channel_column):
    name=c.normalize_title_subtitles(ch[0])
    dbAdapter.update_channel(name,ch[1])   
dbAdapter.close()
print("finalizada consulta")
"""

#------------------------------------------------------
#INDEXACIÓN NUEVOS SUBTÍTULOS
#------------------------------------------------------
"""
from modules.sql import dBAdapter
dbAdapter = dBAdapter.Database()
dbAdapter.open()
names_db=dbAdapter.selectAllNames()
names_db_list=[ndb[0] for ndb in names_db]
dbAdapter.close()

from modules.pre import get_data as g
from modules.pre import create_corpus as c
[files, max_files]=g.get_NameFiles()
print("get_data")
dic_subtitles = g.get_data(max_files)
total_subtitles = list(dic_subtitles.keys())
norm_names={}
for key,value in dic_subtitles.items():
    norm_names[c.normalize_title_subtitles(str(key))]=value

dic_sub2add = {sub:value for sub,value in norm_names.items() if sub not in names_db_list}

[new_generator_normalize, new_dic_subtitles]=c.create_corpus_by_dict(dic_sub2add)

def removing_none_words(word):
    if word != None:
        return word
gn=[]
for d in new_generator_normalize:
    gn.append(','.join(list(filter(removing_none_words,d))))


subtitles=list(dic_sub2add.keys())
dbAdapter= dBAdapter.Database()
dbAdapter.open()
for i in range(len(subtitles)):
    date=c.get_date(subtitles[i])
    dbAdapter.insert(subtitles[i], dic_sub2add[subtitles[i]], date)
    dbAdapter.update_generator_normalize(subtitles[i], gn[i])
dbAdapter.close()

#indexación del canal----------------------------------------------------------

import modules.variables as v
channels = v.CHANNELS

channel_column = [(subtitle, channel) for subtitle in list(dic_subtitles.keys()) 
                    for channel in channels if subtitle.find(channel)!=-1 ]

print("vamos a usar la base de datos")
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
from tqdm import tqdm
for ch in tqdm(channel_column):
    name=c.normalize_title_subtitles(ch[0])
    dbAdapter.update_channel(name,ch[1])   
dbAdapter.close()
print("finalizada consulta")

#HACER EN LA BASE DE DATOS LA SIGUIENTE CONSULTA DESPUES DE EJECUTAR EL CÓDIGO
#update tv_storage set state = 'inactive'  WHERE body = '';
    
"""
"""
#------------------------------------------------------
#GET DDBB generator_normalalize from tv_storage
#------------------------------------------------------
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
listado=dbAdapter.selectGenerator_normalize_limit(5)
dic_subtitles = dict(dbAdapter.selectDic_subtitles_limit(5))
dbAdapter.close()
print("finalizada consulta")

generator_normalize = []
for l in listado:
    generator_normalize.append(l[0].split(","))
for gn in generator_normalize:
    while True:
        try:
            gn.remove("")
        except ValueError:
            break

#------------------------------------------------------
#GET DDBB DOC2VEC prueba
#------------------------------------------------------
dbAdapter.open()
listado=dbAdapter.select_dataDoc2Vec(5622)
dbAdapter.close()
print("finalizada consulta")
listado2=[]
for l in listado:
    listado2.append(l[0].split(","))
for l in listado2:
    while True:
        try:
            l.remove("")
        except ValueError:
            break


#------------------------------------------------------
#COMPROBACIÓN FUNCIONAMIENDTO NORMALIZE WORDS
#------------------------------------------------------
from modules.pre import create_corpus as c
word="microsoft"
change = c.normalize_word(word)
"""
"""
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
results=dbAdapter.selectDict()
dbAdapter.close()
dresults=dict(results)

from modules.pre import create_corpus as c
from tqdm import tqdm
from nltk import word_tokenize
print("\n tokenizing words ...")
list_subt_token = [word_tokenize(value) for (key,value) in tqdm(dresults.items())]
print("\n Creation of generator normalize")
generator_normalize = [list(c.normalize(document)) for document in tqdm(list_subt_token)]
generator_normalize = list(generator_normalize)

from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
print("inserting into database generator_normalize...")
for i in tqdm(range(len(list(dresults.keys())))):
    dbAdapter.open()
    results=dbAdapter.insert_generator(list(dresults.keys())[i],generator_normalize[i])
    dbAdapter.close()


prueba=dresults['1_spa_2016 11 29_morning_new']
prueba_t=word_tokenize(prueba)
normalize=list(c.normalize(prueba_t))
"""
"""
----------------------------------------------------
INTENTAR INSERTAR MODELO LDA EN LA BASE DE DATOS
-----------------------------------------------------
import pickle
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
n_documents=9
n_topics=9
file_lda_model = 'pickle\\'+str(n_documents)+'\lda_model_'+str(n_topics)+'_'+str(n_documents)+'.bin'
f = open(file_lda_model,'rb')
fstring=f.read()
dbAdapter.open()
print("insertar lda model")
dbAdapter.insertLdaModel("lda9",str(fstring),fstring )
print("extraer lda model")
lda=dbAdapter.selectLdaModelByName("lda9")
dbAdapter.close()

f.close()
file_lda_model = 'pickle\\'+str(n_documents)+'\corpus_'+str(n_documents)+'.txt'
f=open(file_lda_model, 'rb')
corpus = pickle.load(f)
f.close()
-----------------------------------------------------
"""
"""
#----------------------------------------------------
#IMPORTACION DICTIONARIO Y GENERATOR_NORMALIZE DE LA BASE DE DATOS
#-----------------------------------------------------
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
dic_subtitles = dict(dbAdapter.selectDic_subtitles_limit(200))
gn = dbAdapter.selectGenerator_normalize_limit(200)
generator_normalize = [gni[0] for gni in gn]
dbAdapter.close()
#-----------------------------------------------------

from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
max_columns= int(dbAdapter.get_maxDocuments()[0][0]);
dbAdapter.close()
"""
"""

from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
key='1_spa_2016 11 06_afternoon_new'
result = dbAdapter.selectRowByName(key)
date=c.get_date(key)
dbAdapter.insert(key,dic_subtitles[key].replace("'",""),date)
dbAdapter.close()
"""
"""
from tqdm import tqdm
from nltk import word_tokenize
print("\n tokenizing words ...")
list_subt_token = [word_tokenize(value) for (key,value) in tqdm(dic_subtitles.items())]
print("\n Creation of generator normalize")
generator_normalize = [list(c.normalize(document)) for document in tqdm(list_subt_token)]
generator_normalize = list(generator_normalize)
"""
