# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 09:17:35 2020

@author: cvicentm
"""

import logging
from modules.sql import helpers as h

class Database:   
    
    def __init__(self,name_database,name_collection):
        
        #-------------------------------------
        import configparser
        config = configparser.ConfigParser()
        config.read('config\\config.ini')
        #-------------------------------------
        self.host = config['DATABASE_MONGO']['host']
        self.port = int(config['DATABASE_MONGO']['port'])
        self.name_database = name_database
        self.name_collection = name_collection

    def open(self):
        from pymongo import MongoClient
        self.client = MongoClient(self.host, self.port)
        self.database = self.client[self.name_database]
        self.collection = self.database[self.name_collection]
    
    def close(self):
        self.client.close()
        
    #SELECTS-------------------------------------------------------------------
    def get_maxDocuments(self):
        from mysql.connector import Error
        
        try:
        
            self.cursor = self.collection.find({},{"Index":1}).count()
    
            return self.cursor
    
        except:
            
            logging.warning("Error in function get_maxDocuments")
            
    def get_maxDocuments_activate(self):
        from mysql.connector import Error
        
        try:
        
            self.cursor = self.collection.find({ "state" : 'active' },{"Index":1}).count()
    
            return self.cursor
    
        except:
            
            logging.warning("Error in function get_maxDocuments_activate")
    
    
    def selectDict(self):
        
        try:
        
            self.cursor = self.collection.find({}, {
                "name": 1,
                "subtitle": 1
            }).limit(10)
            
            return self.cursor
            
        except:
            
            logging.warning("Error reading table "+str(self.name_collection)+" using mongo at query:")
    
    def selectRowByName(self, name):
        try:
        
            self.cursor = self.collection.find({'name': name }, {
                'name': 1,
                'subtitle': 1
            })
            
            return self.cursor
        except:
            
            logging.warning("Error in function selectRowByName")
    
    def selectAllNames(self):
    
        try:
            self.cursor = self.collection.find({}, {
                'name': 1
            })
            
            return self.cursor
        except:
            logging.warning("Error in function selectAllNames")
    
    def selectAll(self,limit):
        
        try:
            self.cursor = self.collection.find({}).limit(int(limit))
            
            return self.cursor
        except:
            logging.warning("Error in function selectAll")
    
    
    def selectDic_subtitles_limit(self, limit):
        from mysql.connector import Error
        
        try:
        
            self.cursor = h.mongo_q_to_dict(self.collection.find({"state":{"$ne":"inactive"}},{"name":1,"subtitle":1}).limit(int(limit)))
            
            return self.cursor
        except:
            logging.warning("Error in function selectDic_subtitles_limit")
            
    
    def selectGenerator_normalize_limit(self, limit):
        
        try:

            self.cursor = h.mongo_q_generator_normalize_to_list(list(self.collection.find({"state":{"$ne":"inactive"}},{"normalize":1}).limit(int(limit))))
            
            return self.cursor
        except:
            logging.warning("Error in function selectGenerator_normalize_limit")
            
 
    def select_dataDoc2Vec(self, limit):       
        try:
            
            self.cursor = h.mongo_q_doc2vec_to_list(self.collection.find({"state":{"$ne":"inactive"}},{"doc2vec":1}).limit(int(limit)))
            
            return self.cursor
        except:
            logging.warning("Error in function select_dataDoc2Vec")
    
    def selectAllByName(self, name):
        try:
        
            self.cursor = self.collection.find({'name': name }, {
                        'Index':1,
                        'normalize':1,
                        'subtitle':1,
                        'doc2vec':1,
                        'channel':1,
                        'name':1,
                        'day':1
                    })
            
            return self.cursor
        except:
            
            logging.warning("Error in function selectRowByName")
    
    
    #END_SELECTS---------------------------------------------------------------
    
    #UPDATES-------------------------------------------------------------------
    def update_doc2vec(self, name, value):            
        try:

            self.cursor = self.collection.update({"name": name},{"$set":{"doc2vec":value}})

        except:
            logging.warning("Error in function update_doc2vec")
            
    
    def update_subtitle(self, name, value):  
        value = str(value.replace("'",""))
        
        try:
            self.cursor = self.collection.update({"name": name},{"$set":{"subtitle":value}})

        except:
            logging.warning("Error in funcition update_subtitle")
            
    
    def update_date(self, name, value):
        date = str(value.replace("'",""))
            
        try:

            self.cursor = self.collection.update({"name": name},{"$set":{"date":value}})

        except:
            logging.warning("Error in funcition update_date")
    
    def update_channel(self, name, value):
            
        try:

            self.cursor = self.collection.update({"name": name},{"$set":{"channel":value}})

        except:
            logging.warning("Error in funcition update_channel")
    
    def update_normalize(self, name, value):

        value = str(value).replace('"','')
            
        try:

            self.cursor = self.collection.update({"name": name},{"$set":{"normalize":value}})

        except:
            logging.warning("Error in funcition update_channel")
    #END_UPDATES---------------------------------------------------------------