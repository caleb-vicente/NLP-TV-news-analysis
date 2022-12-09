# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 19:52:10 2020

@author: cvicentm
"""
import timeit
#modulos propios

from modules import sql
import statistics 
from tqdm import tqdm


tic=timeit.default_timer()
#IMPORTACIÓN DE TODOS LOS DATOS SOBRE SQL
def sql_function_max():
    tic = timeit.default_timer()
    dbAdapter = sql.dBAdapter_sql.Database()
    dbAdapter.open()
    max_documentos = dbAdapter.get_maxDocuments()
    #int(max_documents[0][0])
    result_sql = dbAdapter.selectAll(100)
    dbAdapter.close()
    toc = timeit.default_timer()
    
    return toc-tic

def mongo_function_max():
    tic = timeit.default_timer()
    database = 'tfg_project'
    collection = 'tv_storage'
    dbAdapter = sql.dBAdapter.Database(database, collection)
    dbAdapter.open()
    max_documents = dbAdapter.get_maxDocuments()
    result_mongo = list(dbAdapter.selectAll(100))
    dbAdapter.close()
    toc = timeit.default_timer()
    
    return toc-tic

def sql_function_limit(limit):
    tic = timeit.default_timer()
    dbAdapter = sql.dBAdapter_sql.Database()
    dbAdapter.open()
    result_sql = dbAdapter.selectAll(limit)
    dbAdapter.close()
    toc = timeit.default_timer()
    
    return toc-tic

def mongo_function_limit(limit):
    tic = timeit.default_timer()
    database = 'tfg_project'
    collection = 'tv_storage'
    dbAdapter = sql.dBAdapter.Database(database, collection)
    dbAdapter.open()
    result_mongo = list(dbAdapter.selectAll(limit))
    dbAdapter.close()
    toc = timeit.default_timer()
    
    return toc-tic
#START: Con el maximo de documentos-----------------------------
"""
sql_array = []
mongo_array = []

for i in tqdm(range(10)):
    print("Consulta de SQL")
    time_sql = sql_function_max()
    print("Consulta de Mongo")
    time_mongo = mongo_function_max()
    sql_array.append(time_sql)
    mongo_array.append(time_mongo)
    
mean_sql = statistics.mean(sql_array) 
mean_mongo = statistics.mean(mongo_array) 
"""
#END: Con el maximo de documentos--------------------------------


#START: Con el límite de documentos-----------------------------
mean_sql_limit = []
mean_mongo_limit = []
for limit in range(100,9000,500):
    print("Se esta entrenando con:"+str(limit)+"documentos")
    sql_array_limit = []
    mongo_array_limit = []
    for i in tqdm(range(10)):
        print("Consulta de SQL")
        time_sql_limit = sql_function_limit(limit)
        print("Consulta de Mongo")
        time_mongo_limit = mongo_function_limit(limit)
        sql_array_limit.append(time_sql_limit)
        mongo_array_limit.append(time_mongo_limit)
        
    mean_sql_limit.append(statistics.mean(sql_array_limit)) 
    mean_mongo_limit.append(statistics.mean(mongo_array_limit))
#END: Con el límite de documentos-----------------------------
    
#Graficas para ver los tiempos en mongo y sql de consulta en función del número de 
#elementos consultados

import matplotlib.pyplot as plt

graph = plt.figure()

x = range(100,9000,500)
plt.xlabel('Numero de documentos seleccionados')
plt.ylabel('tiempo de ejecucion (s)')
plt.plot(x, mean_sql_limit, 'bx-', label = "consulta sql")
plt.plot(x, mean_mongo_limit, 'rx-', label = "consulta mongo")
plt.legend()

graph.show()


