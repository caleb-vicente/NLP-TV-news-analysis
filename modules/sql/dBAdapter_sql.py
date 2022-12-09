# -*- coding: utf-8 -*-
"""
Created on Sun May 31 08:15:11 2020

@author: cvicentm
"""

import logging

class Database:
    
    
    
    def __init__(self):
        
        #-------------------------------------
        import configparser
        config = configparser.ConfigParser()
        config.read('config\\config.ini')
        #-------------------------------------
        self.host = config['DATABASE']['host']
        self.database = config['DATABASE']['database']
        self.user = config['DATABASE']['user']
        self.password = config['DATABASE']['password']
        
        

    def open(self):
        import mysql.connector
        self.connection = mysql.connector.connect(host= self.host,
                                                 database= self.database,
                                                 user=self.user,
                                                 password=self.password)
    
    
    def get_maxDocuments(self):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT count(id) FROM tv_storage"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table tv_storage at query:"+str(sql))
    
    def get_maxDocuments_active(self):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT count(id) FROM tv_storage where state = 'active'"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table tv_storage at query:"+str(sql))
    
    #START: SELECT INFO FROM DATABASE------------------------------------------------------------------------------    
    def selectRowByName(self, name):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT name,body FROM tv_storage WHERE name = "+"'"+str(name)+"';"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table prueba at query:"+str(sql))
            
        
            
            
    def insert(self, key, value, date):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        dbAdapter = Database()
        dbAdapter.open()
        result = dbAdapter.selectRowByName(key)
        dbAdapter.close()
        if len(result)==0: 
            date = "'"+date+"'"
            name = "'"+key+"'"
            body = "'"+str(value.replace("'",""))+"'"
            state = "'inactive'"
            if body != "":
                state = "'active'"
            
            try:
            
                sql = "INSERT INTO tv_storage (name,state,date,body) VALUES ("+name+", "+state+", "+date+" ,"+body+");"
                self.cursor = self.connection.cursor()
                self.cursor.execute(sql)
                #without using commit function is imposible insert but it is not neccesary to do a select
                self.connection.commit()
            
            
            except Error as e:
                print("Error inserting into table tv_storage "+str(name))
                logging.warning("Error inserting into table tv_storage "+str(name))
    
    def update_body(self, name, value):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        name = "'"+str(name)+"'"
        body = "'"+str(value.replace("'",""))+"'"
            
        try:
        
            sql = "update tv_storage set body = "+body+" WHERE name = "+name+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table tv_storage body: "+str(name))
        
    def update_date(self, name, value):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        name = "'"+str(name)+"'"
        date = "'"+str(value.replace("'",""))+"'"
            
        try:
        
            sql = "update tv_storage set date = "+date+" WHERE name = "+name+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table tv_storage date: "+str(name))
            
    def update_channel(self, name, value):
        "this function insert a channel into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        name = "'"+str(name)+"'"
        body = "'"+str(value)+"'"
            
        try:
        
            sql = "update tv_storage set channel = "+body+" WHERE name = "+name+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table tv_storage channel: "+str(name))
                
    def insert_dataDoc2Vec(self, name, value):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        name = "'"+name+"'"
        value = '"'+str(value).replace("'","").replace('"','')+'"'
            
        try:
        
            sql = "update tv_storage set data_doc2vec = "+value+" WHERE name = "+name+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table tv_storage doc2vec: "+str(name))
    
    def update_generator_normalize(self, name, value):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        name = "'"+name+"'"
        value = '"'+str(value)+'"'
            
        try:
        
            sql = "update tv_storage set normalize_text = "+value+" WHERE name = "+name+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table tv_storage generator_normalize: "+str(name))
            
    def insert_dataDoc2Vec_prueba(self,value):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        value = "'"+value.replace("'","").replace('"','')+"'"
            
        try:
        
            sql = "INSERT INTO prueba (doc2vec) VALUES ("+value+");"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table prueba datadoc2vec: ")
    
    def select_dataDoc2Vec_prueba(self, limit):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT doc2vec FROM prueba LIMIT "+str(limit)+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table prueba at query:"+str(sql))
                
    def update_generator(self, name, value):
        "this function insert a row into tv_storage if that row doesnt exist"
        from mysql.connector import Error;
        name = "'"+name+"'"
        value = '"'+str(value).replace('"','')+'"'
            
        try:
        
            sql = "update tv_storage set normalize_text = "+value+" WHERE name = "+name+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table tv_storage generator_normalize: "+str(name))

            
    def selectDict(self):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT name,body FROM tv_storage;"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table tv_storage at query:"+str(sql))
    
    def selectAllNames(self):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT name FROM tv_storage;"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table tv_storage at query:"+str(sql))
    
    def selectAll(self,limit):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT * FROM tv_storage LIMIT "+str(limit)+";"
            #sql = "SELECT name,date,state,body FROM tv_storage LIMIT "+str(limit)+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            print(sql)
            logging.warning("Error reading table tv_storage at query:"+str(sql))
            
            

    def selectDic_subtitles_limit(self, limit):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT name,body FROM tv_storage WHERE state != 'inactive' LIMIT "+str(limit)+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table prueba at query:"+str(sql))
            
            
    def selectGenerator_normalize_limit(self, limit):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT normalize_text FROM tv_storage WHERE state != 'inactive' LIMIT "+str(limit)+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table prueba at query:"+str(sql))
    
    def select_dataDoc2Vec(self, limit):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT data_doc2vec FROM tv_storage WHERE state != 'inactive' LIMIT "+str(limit)+";"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table prueba at query:"+str(sql))
    
    #START lda model------------------------------------------------------------------------------------------------
    def insertLdaModel(self, name, value, binary_model):
        "this function insert a row into tv_storage if that row doesnt exist"
        print("hola")
        from mysql.connector import Error;
        import MySQLdb
        name = name
        value = value
        try:
        
            sql = "INSERT INTO prueba (name, lda, binary_model) VALUES (%s,%s,%s);"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql,(name,value,MySQLdb.escape_string(binary_model)))
            #without using commit function is imposible insert but it is not neccesary to do a select
            self.connection.commit()
        
        
        except Error as e:
            print("Error", e)
            logging.warning("Error inserting into table prueba model: "+str(name))
            
    def selectLdaModelByName(self, name):
        from mysql.connector import Error
        
        try:
        
            sql = "SELECT lda, binary_model FROM prueba WHERE name = "+"'"+str(name)+"';"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table lda at query:"+str(sql))
    
    def selectAllInnerJoinById(self,number):
        from mysql.connector import Error
        
        try:
        
            sql = 'SELECT subtitles.*, body.body,normalize.normalize,doc2vec.doc2vec from subtitles inner join body on subtitles.id = body.subtitles_id inner join normalize on subtitles.id = normalize.subtitles_id inner join doc2vec on subtitles.id = doc2vec.subtitles_id  where subtitles.name = "'+str(number)+'";'
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            
            return self.cursor.fetchall()
            #without using commit function is imposible insert but it is not neccesary to do a select        
        
        except Error as e:
            
            logging.warning("Error reading table lda at query:"+str(sql))
    #END lda model------------------------------------------------------------------------------------------------

    
    def close(self):
        
        if (self.connection.is_connected()):
            self.connection.close()
            self.cursor.close()
            
