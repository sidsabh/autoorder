"""
This is the main code. Our program uses the flask web framework in combination with Twilio's/Plivo's API for sending sms messages
to enable text message ordering for restaurants.
This file is mainly for parsing the database to find the user and define global variables.
"""

import g

from flask import Flask, request, session

import pymongo
from pymongo import MongoClient

from primary_methods import *
from methods import *
from order_index import *


#setup database, go straight to the index database
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
index_db = cluster["Index"]
onc = index_db["our_numbers"]
unc = index_db["user_numbers"]


#setup flask app
app = Flask(__name__)
app.config.from_object(__name__)


#entry point for when message comes in
@app.route("/sms", methods=['GET', 'POST'])
def main():

    #get the message that was sent and make it all lowercase
    #CHANGE TO 'Text' WHEN USING PLIVO 
    g.msg = request.values.get('Body', None)
    g.msg = g.msg.lower()

    #get the phone number of the incoming msg
    g.from_num = request.values.get('From', None)
    
    #get the phone number the message was sent to
    g.to_num = request.values.get('To', None)

    #if the user does not have a profile in our database
    if not unc.find_one({"_id":g.from_num}):
        unc.insert_one({"_id":g.from_num, "current_order":None})
    
    #get the documents of the user and the number they are texting
    from_profile = unc.find_one({"_id":g.from_num})
    to_profile = onc.find_one({"_id":g.to_num})
    
    #if the user is known to be in the middle of an order
    if from_profile["current_order"]:

        #set some global variables based on code
        rdb = cluster["{code}".format(code=from_profile["current_order"])]
        g.opc = rdb["order_process"]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #go do the things
        return order_index()


    #THE NEXT PART OF THE CODE TRIES TO FILL IN THE CURRENT ORDER


    #if the number only has one restaurant attached to it
    if len(to_profile["codes"]) == 1:
        from_profile["current_order"] = to_profile["codes"][0]

        #update the database
        unc.update_one({"_id":g.from_num}, {"$set":{"current_order":from_profile["current_order"]}})

        #set some global variables based on code
        rdb = cluster["{code}".format(code=from_profile["current_order"])]
        g.opc = rdb["order_process"]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #do the thing
        return order_index()

    #keyword search, start to construct response
    resp = to_profile["index_message"]+" Your options are: \n"
    for code in to_profile["codes"]:
        db = cluster["{code}".format(code=code)]
        infoc = db["info"]
        resp += "\n{name}".format(name=infoc.find_one({"_id":"info"})["name"])
        for name in infoc.find_one({"_id":"info"})["names"]:
            if is_similar(name):
                from_profile["current_order"] = code

    #if the keyword search worked
    if from_profile["current_order"]:

        #update the database
        unc.update_one({"_id":g.from_num}, {"$set":{"current_order":from_profile["current_order"]}})

        #set some global variables based on code
        rdb = cluster["{code}".format(code=from_profile["current_order"])]
        g.opc = rdb["order_process"]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #do the thing
        return order_index()

    #if the program fails to fill in the current order, send an index message
    else:
        return send_message(resp)




if __name__ == "__main__":
    app.run(debug=True)
