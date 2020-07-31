"""
This file is where we store global variables. They are updated as the info comes in.
"""

import pymongo
from pymongo import MongoClient


#setup database, go straight to the index database
CLUSTER = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
INDEX_DB = CLUSTER["Index"]
ONC = INDEX_DB["our_numbers"]
UNC = INDEX_DB["user_numbers"]
OPC = INDEX_DB["order_process"]
RC = INDEX_DB["restaurants"]
OC = INDEX_DB["orders"]


#The user's phone number
from_num = None

#The number the user texted
to_num = None

#The message the user sent
msg = None


#The menu of the current restaurant
menu = None

#The info of the current restaurant
info = None

#The code of the current restaurant
code = None


