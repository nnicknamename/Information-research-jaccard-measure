import string
from pymongo import MongoClient

from Data.Corpus import *

class Database:
    def __init__(self,password):
        self.dbname=self.get_database(password)

    def get_database(self,password):
        CONNECTION_STRING = "mongodb+srv://Admin:"+password+"@cluster0.dowv2vn.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(CONNECTION_STRING, connect=False)
        return client["Corpus"]
    def Insert_Corpus(self,corpus:Corpus):
        assert self.dbname.list_collection_names().count('carn')==0 ,"collection already exists"
        collection_name = self.dbname[corpus.name]
        collection_name.insert_many(corpus.documents)
        
    def get_collection(self,name):
        assert self.dbname.list_collection_names().count(name)==1 ,"collection does not exist"
        return  self.dbname[name]