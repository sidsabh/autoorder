from flask import Blueprint, render_template, jsonify, request, send_file
from flask_login import login_required, current_user
import time
import string
import random
from bson.json_util import dumps
import pymongo
from pymongo import MongoClient


from .settings import *
from .essentials import *

from flask import Flask, request, session, render_template, abort

from .info import *
from .messaging import *
from .order_index import *

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

#site for error handling
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

#setup site for error handling
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

main = Blueprint('main', __name__)
mongo = MongoClient('mongodb://orders:orders!1@ds261077.mlab.com:61077/heroku_8qfx8bg5?retryWrites=false')
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")

orders_db = cluster["0000"]
orders_collection = orders_db["orders"]

"""
Deletes active orders that are more than 20 minutes old.
"""


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
            OPC.delete_one({"_id": order["_id"]})


#create scheduler that runs the delete_old function every 30 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old, trigger="interval", seconds=30)
scheduler.start()


@main.route('/')
def index():
    return render_template('sign-in.html')


@main.route('/access/')
@login_required
def dashboard():
    return render_template('index.html', name=current_user.name)


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@main.route('/orders')
def orders():
    return render_template("orders.html")


def total_cost(item_list):
    cost = 0
    for item in item_list:
        cost += item["main_item"]["base_price"]
        for sublist in item["main_item"]["adds_list"]:
            for subitem in item[sublist["name"]]:
                cost += subitem["add_price"]
    return cost

def pricify(price):
    if float(price).is_integer():
        price = int(price)
        resp = "${price}".format(price=price)
    elif (price/0.1).is_integer():
        resp = "${price}0".format(price=price)
    else:
        resp = "${price}".format(price=price)
    return resp

def stringify_order(item_list):
    resp = ""
    for item in item_list:
        item_str = "\n\n1x {main_name} ".format(main_name=item["main_item"]["name"])
        if len(item["main_item"]["adds_list"]) > 0:
            item_str += "\n"
            #item_str += "("
            for sublist in item["main_item"]["adds_list"]:
                item_str += "{sub_name}: ".format(sub_name=sublist["name"])
                for subitem in item[sublist["name"]]:
                    item_str += "{name}".format(name=subitem["name"])
                    if subitem == item[sublist["name"]][-1]:
                        item_str += ". "
                    else:
                        item_str += ", "
            item_str = item_str[:-1]
            #item_str += ")"
        resp += item_str
    #resp += " \n\nTOTAL COST: {cost}".format(cost=pricify(total_cost()))
    return resp



@main.route('/api/orders/poll')
def poll():
    cursor = orders_collection.find({})
    orders = []
    for document in cursor:
        orders.append({
            "from_num": document["from_num"],
            "item_list": stringify_order(document["item_list"]),
            "method_of_getting_food": document["method_of_getting_food"],
            "address": document["address"],
            "comments": document["comments"],
            "timestamp": document["timestamp"],
            "total": total_cost(document["item_list"])
        })
    return jsonify(orders)


"""
Endpoint to add orders

POST JSON
{
    "customer": "7558894849",
    "items": [
        ("Hotdog": 1.99),
        ("Coke": 0.99),
    ]
}

RETURN
{
    "order_id": "asdfasdf",
}

"""
@main.route('/api/orders/add', methods=['POST'])
def add():
    order = {
        "customer": request.json['customer'],
        "items": request.json['items']
    }
    order['timestamp'] = int(time.time())
    total = 0
    for item in order["items"]:
        total += item[1]
    order["total"] = total
    order_id = get_random_string(8)
    order["order_id"] = order_id
    mongo.heroku_8qfx8bg5.orders.insert_one(order)
    return jsonify({"order_id": order_id})


"""
Endpoint to add orders

POST JSON
{
    "order_id": "asdfasdf"
}

RETURN
200

"""
@main.route('/api/orders/remove', methods=['POST'])
def remove():
    orders_collection.delete_one({"timestamp": request.json["timestamp"], "from_num": request.json["from_num"]})
    return "", 200


@main.route('/checkout/<id>')
def checkout(id):
    stripe_type = id[0:8]
    if stripe_type == "cs_live_":
        return render_template('checkout.html', SESSION_ID=id, PUBLIC_KEY='pk_live_51H7n9PDTJ2YcvBWsuSJNpWfVJQXNuQWOyTQNrBbjrjvJwcbA02SiRrMMr1QbZqpG5YtzgpOe88wsZ0u3BjAbVFqu00RjOt8mga')
    elif stripe_type == "cs_test_":
        return render_template('checkout.html', SESSION_ID=id, PUBLIC_KEY='pk_test_51H7n9PDTJ2YcvBWsgWnXQ3VC2Wh4EbN41ftVHS3hnxLTl2TEZyRUnUcFvpj3B89xsmNEeXJK0PgYhBAezna4iVP800Vrcrphbq')


@main.route('/success/')
def success():
    return send_file('static/img/Success3.jpeg', attachment_filename='Success3.jpeg')


@main.route('/testaurant/')
def testaurant():
    return send_file('static/img/Testaurant.jpg', attachment_filename='Testaurant.jpg')


@main.route('/ozuramen/')
def ozuramen():
    return send_file('static/img/OzuRamen.jpg', attachment_filename='OzuRamen.jpg')


@main.route('/failure/')
def failure():
    return "An error has occurred."


@main.route('/.well-known/acme-challenge/ioEW6yGfJ2mw88WOzHnjWN3aVNevNvdEQLvyrOtn7o0')
def ioEW6yGfJ2mw88WOzHnjWN3aVNevNvdEQLvyrOtn7o0():
    return "ioEW6yGfJ2mw88WOzHnjWN3aVNevNvdEQLvyrOtn7o0.CtFmA8tprSQo_fU2zmocKZdXMwbEfAHW_6QJ7r8UELg"

#entry point for when message comes in
@main.route("/sms", methods=['GET', 'POST'])
def sms():

    #setup a class to store the basic info (message, from number, to number, rinfo will be updated)
    msg = Info(txt=request.values.get('Body').lower(), fro=request.values.get(
        'From', None), to=request.values.get('To', None), rinfo=None)

    #if the user does not have a profile in our database (this is how we will collect data on users in the future)
    if not UNC.find_one({"_id": msg.fro}):
        UNC.insert_one({"_id": msg.fro})

    #get info about the number the user texted
    to_profile = ONC.find_one({"_id": msg.to})

    #if the user is known to be in the middle of an order with the number they texted
    if current_order(msg):

        #reset time
        OPC.update_one(current_order(msg), {
                       "$set": {"timestamp": str(datetime.datetime.today())}})

        #setup the current restaurant's info
        msg.rinfo = RC.find_one({"_id": current_order(msg)["code"]})

        #if the user texted "index" and there is an index then delete the order and the user will return to the index
        if len(to_profile["codes"]) > 1 and msg.txt == "index":
            OPC.delete_one(current_order(msg))

        else:
            #go do the things
            return order_index(msg)

    #Try to fill in current order

    #if the number only has one restaurant attached to it
    if len(to_profile["codes"]) == 1:

        #initialize order object
        OPC.insert_one({"from_num": msg.fro, "to_num": msg.to, "code": to_profile["codes"][0], "timestamp": str(datetime.datetime.today(
        )), "section": "first", "sublist_in_q": None, "item_list": [], "method_of_getting_food": "pickup", "address": None, "comments": None, "payment_intent": None})

        #setup the current restaurant's info
        msg.rinfo = RC.find_one({"_id": current_order(msg)["code"]})

        #do the thing
        return order_index(msg)

    #see if the user typed in any of keyword of a restaurant in the index, also build response if it fails
    resp = to_profile["index_message"]+" Your options are: \n"
    #iterate through the codes attached to the number the user texted
    for code in to_profile["codes"]:

        #find the restaurant with the corresponding code
        restaurant = RC.find_one({"_id": code})

        #add the restaurant's name to the reply
        resp += "\n{name}".format(name=restaurant["name"])

        #iterate through the keywords attached to the code
        for name in restaurant["names"]:

            #if the user did enter a keyword
            if is_similar(msg, name):
                #initialize order object
                OPC.insert_one({"from_num": msg.fro, "to_num": msg.to, "code": code, "timestamp": str(datetime.datetime.today()), "section": "first",
                                "sublist_in_q": None, "item_list": [], "method_of_getting_food": "pickup", "address": None, "comments": None, "payment_intent": None})

                #setup the current restaurant's info
                msg.rinfo = RC.find_one({"_id": current_order(msg)["code"]})

                #go do the things
                return order_index(msg)

    #if the program fails to fill in the current order, send the index message
    return send_message(resp)

#Stripe webhook for when payment is completed
@main.route("/checkedout/<mode>", methods=['POST'])
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

        #get the session
        session = event['data']['object']

        #get the unique payment intent id
        pi = session["payment_intent"]

        #get the order the payment intent corresponds to
        correct_order = OPC.find_one({"payment_intent": pi})

        #get the restaurant
        correct_restaurant = RC.find_one({"_id": correct_order["code"]})

        #craft and send a message
        if correct_order["method_of_getting_food"] == "pickup":
            resp = "Your order has been processed! Your food will be ready for pickup in about {min} minutes.".format(
                min=correct_restaurant["pickup_time"])
        if correct_order["method_of_getting_food"] == "delivery":
            resp = "Your order has been processed! Your food will be delivered in about {min} minutes.".format(
                min=correct_restaurant["delivery_time"])
        send_message_client(
            resp, correct_order["from_num"], correct_order["to_num"])

        #delete the current order
        OPC.delete_one({"payment_intent": pi})

        #insert order into order collection
        OC.insert_one(correct_order)

        #input the order id into the restaurant's orders
        restaurant_orders = correct_restaurant["orders"]
        restaurant_orders.append(correct_order["_id"])
        RC.update_one({"_id": correct_order["code"]}, {
                      "$set": {"orders": restaurant_orders}})

    return {}



atexit.register(lambda: scheduler.shutdown())
