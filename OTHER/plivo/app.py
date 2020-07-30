"""
This is the main code. Our program uses the flask web framework in combination with Twilio's/Plivo's API for sending sms messages
to enable text message ordering for restaurants.
This file is mainly for parsing the database to find the user and define global variables.
"""

import g

from flask import Flask, request, session, render_template, abort

import pymongo
from pymongo import MongoClient

from primary_methods import *
from methods import *
from order_index import *
from more_methods import *

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

import datetime

#setup flask app
app = Flask(__name__)
app.config.from_object(__name__)

#scheduler function to delete all the old orders
def delete_old():

    current_time = datetime.datetime.today()
    items_to_delete = []

    orders = g.opc.find({})
    for order in orders:

        #converts the order time from a string to a datetime
        order_time_str = order["timestamp"]
        form = "%Y-%m-%d %H:%M:%S.%f"
        order_time = datetime.datetime.strptime(order_time_str, form)

        #if the difference between the last time the order was updated and the current time is greater than 20 minutes, delete the order from the database
        difference = current_time - order_time
        if difference.total_seconds()/60 > 20:
            MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")["Index"]["order_process"].delete_one({"_id":order["_id"]})


#create scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old, trigger="interval", seconds=30)
scheduler.start()


#entry point for when message comes in
@app.route("/sms", methods=['GET', 'POST'])
def main():

    #get the message that was sent and make it all lowercase
    #CHANGE TO 'Text' WHEN USING PLIVO 
    g.msg = request.values.get('Body')
    g.msg = g.msg.lower()

    #get the phone number of the incoming msg
    g.from_num = request.values.get('From', None)
    
    #get the phone number the message was sent to
    g.to_num = request.values.get('To', None)

    #if the user does not have a profile in our database
    if not g.unc.find_one({"_id":g.from_num}):
        g.unc.insert_one({"_id":g.from_num})
    

    
    #if the user is known to be in the middle of an order with the number they texted
    if current_order():

        #reset time
        g.opc.update_one(current_order(), {"$set":{"timestamp":str(datetime.datetime.today())}})

        #setup the current restaurant's menu and info
        rdb = g.cluster["{code}".format(code=current_order()["code"])]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #if the user texted "index" then delete the order
        if g.msg=="index":
            g.opc.delete_one(current_order())

        else:
            #go do the things
            return order_index()


    #THE NEXT PART OF THE CODE TRIES TO FILL IN THE CURRENT ORDER

    #get info about the number the user texted
    to_profile = g.onc.find_one({"_id":g.to_num})

    #if the number only has one restaurant attached to it
    if len(to_profile["codes"]) == 1:
        
        #initialize order object
        g.opc.insert_one({"from_num":g.from_num, "to_num":g.to_num, "code":to_profile["codes"][0], "timestamp":str(datetime.datetime.today()), "section":"first", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None, "payment_intent":None})

        #set some global variables based on code
        rdb = g.cluster["{code}".format(code=current_order()["code"])]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #do the thing
        return order_index()


    #see if the user typed in any of keyword of a restaurant in the index, also build response if it fails
    resp = to_profile["index_message"]+" Your options are: \n"
    #iterate through the codes attached to the number the user texted
    for code in to_profile["codes"]:
        db = g.cluster["{code}".format(code=code)]
        infoc = db["info"]
        resp += "\n{name}".format(name=infoc.find_one({"_id":"info"})["name"])
        #iterate through the keywords attached to the code
        for name in infoc.find_one({"_id":"info"})["names"]:

            #if the user did enter a keyword
            if is_similar(name):
                #initialize order object
                g.opc.insert_one({"from_num":g.from_num, "to_num":g.to_num, "code":code, "timestamp":str(datetime.datetime.today()), "section":"first", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None, "payment_intent":None})

                #set some global variables based on code
                rdb = g.cluster["{code}".format(code=current_order()["code"])]
                g.menu = rdb["info"].find_one({"_id":"menu"})
                g.info = rdb["info"].find_one({"_id":"info"})
                return order_index()


    #if the program fails to fill in the current order, send an index message
    else:
        return send_message(resp)



#Stripe webhook for when payment is completed
@app.route("/checkedout", methods=['POST'])
def checkedout():

    print("webhook called!")

    if request.content_length > 1024*1024:
        print("request too large")
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_S2gZaNvumSOmvea1MxpMJ84eBMr63Hge'
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )

    except ValueError as e:
        # Invalid payload
        print("invalid payload!")
        return {}, 400

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("invalid signature!")
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("HI")

        #get the session
        session = event['data']['object']
        
        #get the unique payment intent id
        pi = session["payment_intent"]
        
        #get the order the payment intent corresponds to
        correct_order = g.opc.find_one({"payment_intent":pi})

        db = g.cluster["{code}".format(code=correct_order["code"])]

        #craft and send a message
        if correct_order["method_of_getting_food"] == "pickup":
            resp = "Your order has been processed! Your food will be ready for pickup in about {min} minutes.".format(min=db["info"].find_one({"_id":"info"})["pickup_time"])
        if correct_order["method_of_getting_food"] == "delivery":
            resp = "Your order has been processed! Your food will be delivered in about {min} minutes.".format(min=db["info"].find_one({"_id":"info"})["delivery_time"])   
        send_message_client(resp, correct_order["from_num"], correct_order["to_num"])
        
        #delete the current order
        g.opc.delete_one({"payment_intent":pi})

        oc = db["orders"]
        oc.insert_one(correct_order)



    return {}




#shutdown the scheduler when the app shuts down
atexit.register(lambda: scheduler.shutdown())

#run the flask app
if __name__ == "__main__":
    app.run(debug=True)

