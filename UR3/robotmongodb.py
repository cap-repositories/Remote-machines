# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 10:12:21 2020

@author: Juan David Contreras
"""
import pymongo

class robotdbcontrol:
    
    def __init__(self, usr, pss): 
        self.usr = usr
        self.pss = pss
        self.collection = self.connectDB()
        
    def connectDB(self):
        client = pymongo.MongoClient("mongodb+srv://"+self.usr+":"+self.pss+"@urcluster-wvnkx.mongodb.net/urdb?retryWrites=true&w=majority")
        urdb = client.urdb
        collection = urdb.urcollection
        #collection.delete_many({}) # borra todos los docs
        return collection
    
    def readDB(self,n):
        R = self.collection
        res = R.find_one({"n":n})
        return res

    def sendDB(self,n,f):
        R = self.collection
        data = {"n":n, "f":f}
        res = R.insert_one(data)
        return res.inserted_id
    

