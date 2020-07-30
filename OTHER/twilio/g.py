"""
This file is where we store global variables. They are updated as the info comes in.
"""

import pymongo
from pymongo import MongoClient


#setup database, go straight to the index database
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
index_db = cluster["Index"]
onc = index_db["our_numbers"]
unc = index_db["user_numbers"]
opc = index_db["order_process"]

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


