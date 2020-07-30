from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
import time
import string
import random
from bson.json_util import dumps
from pymongo import MongoClient

main = Blueprint('main', __name__)
mongo = MongoClient(
    'mongodb://orders:orders!1@ds261077.mlab.com:61077/heroku_8qfx8bg5?retryWrites=false')


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


@main.route('/api/orders/poll')
def poll():
    cursor = mongo.heroku_8qfx8bg5.orders.find({})
    orders = []
    for document in cursor:
        orders.append({
            "customer": document["customer"],
            "items": document["items"],
            "timestamp": document["timestamp"],
            "order_id": document["order_id"],
            "total": document["total"]
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
    mongo.heroku_8qfx8bg5.orders.delete_many(
        {"order_id": request.json["order_id"]})
    return "", 200