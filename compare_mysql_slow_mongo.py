# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:58:03 2020

@author: cvicentm
"""

import timeit
#modulos propios

from modules import sql
import statistics 
from tqdm import tqdm

database = 'tfg_project'
collection = 'tv_storage'
dbAdapter_mongo = sql.dBAdapter.Database(database, collection)
dbAdapter_mongo.open()

dbAdapter = sql.dBAdapter_sql.Database()
dbAdapter.open()

def query_sql(name):
    tic = timeit.default_timer()

    result_sql = dbAdapter.selectAllInnerJoinById(name)

    toc = timeit.default_timer()
    
    return toc-tic

def query_mongo(name):
    tic = timeit.default_timer()
    result_mongo = list(dbAdapter_mongo.selectAllByName(name))
    toc = timeit.default_timer()
    
    return toc-tic
    
#busqueda mysql-----------------------------------------------------------------
import mysql.connector
connection = mysql.connector.connect(host= '192.168.1.39',
                                         database= 'news_storage',
                                         user='root',
                                         password='tfg_project')
sqll = "SELECT id FROM subtitles ;"
cursor = connection.cursor()
cursor.execute(sqll)
index = cursor.fetchall()
index = index[0:5]
#busqueda mongo----------------------------------------------------------------
dict_subtitles = sql.helpers.import_dict_and_normalize('tfg_project','tv_storage',len(index))[0]
subtitles = list(dict_subtitles.keys())
    

time_sql_array = []
time_mongo_array = []
time_sql = 0
time_mongo = 0
for i in tqdm(range(len(index))):
    time_sql = query_sql(subtitles[i])+time_sql
    time_mongo = query_mongo(subtitles[i]) + time_mongo
    time_sql_array.append(time_sql)
    time_mongo_array.append(time_mongo)

dbAdapter.close() 

import matplotlib.pyplot as plt

graph = plt.figure()

x = range(1,6)
plt.xlabel('Numero de documentos seleccionados')
plt.ylabel('Tiempo de ejecucion (s)')
plt.plot(x, time_sql_array, 'bx-', label = "consulta sql")
plt.plot(x, time_mongo_array, 'rx-', label = "consulta mongo")
plt.legend()

graph.show()