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

    users = g.unc.find({})
    for user in users:
        keys = user["current_order"].keys()
        for num in keys:
            order_time_str = user["current_order"][num]["time"]
            form = "%Y-%m-%d %H:%M:%S.%f"
            order_time = datetime.datetime.strptime(order_time_str, form)
            difference = current_time - order_time
            if difference.total_seconds()/60 > 20:
                items_to_delete.append({"user":user, "num":num})
                #user["current_order"].pop(num)
                #g.unc.update_one({"_id":user["_id"]}, {"$set":{"current_order":user["current_order"]}})

    for dic in items_to_delete:
        code = dic["user"]["current_order"][dic["num"]]["code"]
        rest_db = g.cluster[code]
        opc2 = rest_db["order_process"]
        opc2.delete_one({"from_num":dic["user"]["_id"]})
        dic["user"]["current_order"].pop(dic["num"])
        g.unc.update_one({"_id":dic["user"]["_id"]}, {"$set":{"current_order":dic["user"]["current_order"]}})



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
        g.unc.insert_one({"_id":g.from_num, "current_order":{}})
    
    #get the documents of the user and the number they are texting
    from_profile = g.unc.find_one({"_id":g.from_num})
    to_profile = g.onc.find_one({"_id":g.to_num})
    
    #if the user is known to be in the middle of an order
    if from_profile["current_order"].get(g.to_num):

        #reset time
        from_profile["current_order"][g.to_num]["time"] = str(datetime.datetime.today())
        g.unc.update_one({"_id":g.from_num}, {"$set":{"current_order":from_profile["current_order"]}})

        #set some global variables based on code
        rdb = g.cluster["{code}".format(code=from_profile["current_order"][g.to_num]["code"])]
        g.opc = rdb["order_process"]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #go do the things
        return order_index()


    #THE NEXT PART OF THE CODE TRIES TO FILL IN THE CURRENT ORDER


    #if the number only has one restaurant attached to it
    if len(to_profile["codes"]) == 1:
        from_profile["current_order"][g.to_num] = {"code":to_profile["codes"][0],"time":str(datetime.datetime.today())}

        #update the database
        g.unc.update_one({"_id":g.from_num}, {"$set":{"current_order":from_profile["current_order"]}})

        #set some global variables based on code
        rdb = g.cluster["{code}".format(code=from_profile["current_order"][g.to_num]["code"])]
        g.opc = rdb["order_process"]
        g.menu = rdb["info"].find_one({"_id":"menu"})
        g.info = rdb["info"].find_one({"_id":"info"})

        #do the thing
        return order_index()

    #keyword search, start to construct response
    resp = to_profile["index_message"]+" Your options are: \n"
    for code in to_profile["codes"]:
        db = g.cluster["{code}".format(code=code)]
        infoc = db["info"]
        resp += "\n{name}".format(name=infoc.find_one({"_id":"info"})["name"])
        for name in infoc.find_one({"_id":"info"})["names"]:
            if is_similar(name):
                from_profile["current_order"][g.to_num] = {}
                from_profile["current_order"][g.to_num]["code"] = code
                from_profile["current_order"][g.to_num]["time"] = str(datetime.datetime.today())

    #if the keyword search worked
    if from_profile["current_order"].get(g.to_num):
        a=from_profile["current_order"].get(g.to_num)
        if a.get("code"):

            #update the database
            g.unc.update_one({"_id":g.from_num}, {"$set":{"current_order":from_profile["current_order"]}})

            #set some global variables based on code
            rdb = g.cluster["{code}".format(code=from_profile["current_order"][g.to_num]["code"])]
            g.opc = rdb["order_process"]
            g.menu = rdb["info"].find_one({"_id":"menu"})
            g.info = rdb["info"].find_one({"_id":"info"})

            #do the thing
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
        session = event['data']['object']
        
        pi = session["payment_intent"]
        print("HI")
        for code in g.codes:
            db=g.cluster["{code}".format(code=code)]
            opc3=db["order_process"]
            correct_order = opc3.find_one({"payment_intent":pi})
            if correct_order:
                if correct_order["method_of_getting_food"] == "pickup":
                    resp = "Your order has been processed! Your food will be ready for pickup in about {min} minutes.".format(min=db["info"].find_one({"_id":"info"})["pickup_time"])
                if correct_order["method_of_getting_food"] == "delivery":
                    resp = "Your order has been processed! Your food will be delivered in about {min} minutes.".format(min=db["info"].find_one({"_id":"info"})["delivery_time"])
                
                send_message_client(resp, correct_order["from_num"], correct_order["to_num"])
                db["orders"].insert_one(correct_order)
                opc3.delete_one({"payment_intent":correct_order["payment_intent"]})

                use = g.unc.find_one({"_id":correct_order["from_num"]})
                use["current_order"].pop(correct_order["to_num"])
                g.unc.update_one({"_id":correct_order["from_num"]}, {"$set":{"current_order":use["current_order"]}})
                break
                



    return {}




#shutdown the scheduler when the app shuts down
atexit.register(lambda: scheduler.shutdown())

#run the flask app
if __name__ == "__main__":
    app.run(debug=True)

