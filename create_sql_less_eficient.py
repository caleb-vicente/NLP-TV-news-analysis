# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:10:00 2020

@author: cvicentm
"""

from modules import sql
from tqdm import tqdm

database = 'tfg_project'
collection = 'tv_storage'
dbAdapter = sql.dBAdapter.Database(database, collection)
dbAdapter.open()
max_documents = dbAdapter.get_maxDocuments()
result_mongo = list(dbAdapter.selectAll(max_documents))
dbAdapter.close()

import mysql.connector
connection = mysql.connector.connect(host= '192.168.1.39',
                                         database= 'news_storage',
                                         user='root',
                                         password='tfg_project')
"""
#Importar a la base de datos de subtitles
for item in tqdm(result_mongo):
    name = "'"+item['name']+"'"
    channel = "'"+item['channel']+"'"
    date = "'"+item['day']+"'"
    state = "'"+item['state']+"'"
    try:
        sql = "INSERT INTO subtitles (name,channel,datee,state) VALUES ("+name+", "+channel+", "+date+" ,"+state+");"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except:
        print(sql)
"""
#------------------------------------------------------------------------------------------------------
#Importar la parte del normalize
from mysql.connector import Error;
name_array = []
body_array = []
for item in tqdm(result_mongo):
    name_array.append(item['name'])
    body_array.append(item['normalize'])
new_body = [element or 'null' for element in body_array]

for i in tqdm(range(len(name_array))):
    
    try:
        
        name = "'"+name_array[i]+"'"
        body = '"'+str(new_body[i]).replace('"','')+'"'
        
        
        sql = "SELECT id FROM subtitles WHERE name = "+str(name)+";"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        subtitles_id = str(result[0][0])
        
        
        sql2 = "INSERT INTO normalize (normalize,subtitles_id) VALUES ("+body+", "+subtitles_id+");"
        cursor = connection.cursor()
        cursor.execute(sql2)
        connection.commit()

    except Error as e:
        print(e)
        
#------------------------------------------------------------------------------------------------------
#Importar la parte del body
from mysql.connector import Error;
name_array = []
body_array = []
for item in tqdm(result_mongo):
    name_array.append(item['name'])
    body_array.append(item['subtitle'])
new_body = [element or 'null' for element in body_array]

for i in tqdm(range(len(name_array))):
    
    try:
        
        name = "'"+name_array[i]+"'"
        body = '"'+str(new_body[i]).replace('"','')+'"'
        
        
        sql = "SELECT id FROM subtitles WHERE name = "+str(name)+";"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        subtitles_id = str(result[0][0])
        
        
        sql2 = "INSERT INTO body (body,subtitles_id) VALUES ("+body+", "+subtitles_id+");"
        cursor = connection.cursor()
        cursor.execute(sql2)
        connection.commit()

    except Error as e:
        print(e)
        
#------------------------------------------------------------------------------------------------------
#Importar la parte del doc2vec
from mysql.connector import Error;
name_array = []
body_array = []
for item in tqdm(result_mongo):
    name_array.append(item['name'])
    body_array.append(item['doc2vec'])
new_body = [element or 'null' for element in body_array]

for i in tqdm(range(len(name_array))):
    
    try:
        
        name = "'"+name_array[i]+"'"
        body = '"'+str(new_body[i]).replace('"','')+'"'
        
        
        sql = "SELECT id FROM subtitles WHERE name = "+str(name)+";"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        subtitles_id = str(result[0][0])
        
        
        sql2 = "INSERT INTO doc2vec (doc2vec,subtitles_id) VALUES ("+body+", "+subtitles_id+");"
        cursor = connection.cursor()
        cursor.execute(sql2)
        connection.commit()

    except Error as e:
        print(e)