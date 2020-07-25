#from flask import Flask, request, session
#from sample_menu import *
#from methods import *
import pymongo
from pymongo import MongoClient
#from primary_methods import *

#import g


#setup database, go straight to the index database
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
index_db = cluster["Index"]
onc = index_db["our_numbers"]
unc = index_db["user_numbers"]

#onc.delete_one({"_id":"+17143847583"})
onc.insert_one({"_id":"14133009369", "codes":["0001", "0002"], "index_message":"Welcome to the random restaurant index!"})

