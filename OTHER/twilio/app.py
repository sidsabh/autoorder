"""
This is the main code. Our program uses the flask web framework in combination with Twilio's/Plivo's API for sending sms messages
to enable text message ordering for restaurants.
This file is mainly for parsing the database to find the user and define global variables.
"""


from settings import *
from essentials import *

from flask import Flask, request, session, render_template, abort

from info import *
from messaging import *
from order_index import *

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

#site for error handling
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

#setup flask app
app = Flask(__name__)
app.config.from_object(__name__)

#scheduler function to delete all the old orders
def delete_old():

    #get current time and initiate a list
    current_time = datetime.datetime.today()
    items_to_delete = []

    #get all orders and iterate through them
    orders = OPC.find({})
    for order in orders:

        #converts the order time from a string to a datetime
        order_time_str = order["timestamp"]
        form = "%Y-%m-%d %H:%M:%S.%f"
        order_time = datetime.datetime.strptime(order_time_str, form)

        #if the difference between the last time the order was updated and the current time is greater than 20 minutes, delete the order from the database
        difference = current_time - order_time
        if difference.total_seconds()/60 > 20:
            OPC.delete_one({"_id":order["_id"]})

#create scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old, trigger="interval", seconds=30)
scheduler.start()



#entry point for when message comes in
@app.route("/sms", methods=['GET', 'POST'])
def main():

    #setup a class to store the basic info (message, from number, to number, rinfo will be updated)
    msg = info(request.values.get('Body').lower(), request.values.get('From', None), request.values.get('To', None), None)

    #if the user does not have a profile in our database (this is how we will collect data on users in the future)
    if not UNC.find_one({"_id":msg.fro}):
        UNC.insert_one({"_id":msg.fro})
    
    #get info about the number the user texted
    to_profile = ONC.find_one({"_id":msg.to})

    #if the user is known to be in the middle of an order with the number they texted
    if current_order(msg):

        #reset time
        OPC.update_one(current_order(msg), {"$set":{"timestamp":str(datetime.datetime.today())}})

        #setup the current restaurant's info
        msg.rinfo = RC.find_one({"_id":current_order(msg)["code"]})
        
        #if the user texted "index" and there is an index then delete the order and the user will return to the index
        if len(to_profile["codes"])>1 and msg.txt=="index":
            OPC.delete_one(current_order(msg))

        else:
            #go do the things
            return order_index(msg)


    #THE NEXT PART OF THE CODE TRIES TO FILL IN THE CURRENT ORDER

    #if the number only has one restaurant attached to it
    if len(to_profile["codes"]) == 1:
        
        #initialize order object
        OPC.insert_one({"from_num":msg.fro, "to_num":msg.to, "code":to_profile["codes"][0], "timestamp":str(datetime.datetime.today()), "section":"first", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None, "payment_intent":None})

        #setup the current restaurant's info
        msg.rinfo = RC.find_one({"_id":current_order(msg)["code"]})

        #do the thing
        return order_index(msg)


    #see if the user typed in any of keyword of a restaurant in the index, also build response if it fails
    resp = to_profile["index_message"]+" Your options are: \n"
    #iterate through the codes attached to the number the user texted
    for code in to_profile["codes"]:

        #find the restaurant with the corresponding code
        restaurant = RC.find_one({"_id":code})

        #add the restaurant's name to the reply
        resp += "\n{name}".format(name=restaurant["name"])

        #iterate through the keywords attached to the code
        for name in restaurant["names"]:

            #if the user did enter a keyword
            if is_similar(msg, name):
                #initialize order object
                OPC.insert_one({"from_num":msg.fro, "to_num":msg.to, "code":code, "timestamp":str(datetime.datetime.today()), "section":"first", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None, "payment_intent":None})

                #setup the current restaurant's info
                msg.rinfo = RC.find_one({"_id":current_order(msg)["code"]})

                #go do the things
                return order_index(msg)


    #if the program fails to fill in the current order, send an index message
    else:
        return send_message(resp)



#Stripe webhook for when payment is completed
@app.route("/checkedout/<mode>", methods=['POST'])
def checkedout(mode):

    print("webhook called!")

    if request.content_length > 1024*1024:
        print("request too large")
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')

    if mode == "live":
        endpoint_secret = STRIPE_LIVE_SECRET_ENDPOINT

    if mode == "test":
        endpoint_secret = STRIPE_TEST_SECRET_ENDPOINT


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
        correct_order = OPC.find_one({"payment_intent":pi})

        #get the restaurant
        correct_restaurant = RC.find_one({"_id":correct_order["code"]})

        #craft and send a message
        if correct_order["method_of_getting_food"] == "pickup":
            resp = "Your order has been processed! Your food will be ready for pickup in about {min} minutes.".format(min=correct_restaurant["pickup_time"])
        if correct_order["method_of_getting_food"] == "delivery":
            resp = "Your order has been processed! Your food will be delivered in about {min} minutes.".format(min=correct_restaurant["delivery_time"])   
        send_message_client(resp, correct_order["from_num"], correct_order["to_num"])
        
        #delete the current order
        OPC.delete_one({"payment_intent":pi})

        #insert order into order collection
        OC.insert_one(correct_order)

        #input the order id into the restaurant's orders
        restaurant_orders = correct_restaurant["orders"]
        restaurant_orders.append(correct_order["_id"])
        RC.update_one({"_id":correct_order["code"]}, {"$set":{"orders":restaurant_orders}})

    return {}



#shutdown the scheduler when the app shuts down
atexit.register(lambda: scheduler.shutdown())

#run the flask app
if __name__ == "__main__":
    app.run(debug=True)

