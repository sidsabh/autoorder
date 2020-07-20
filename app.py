from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
import bcrypt
import time
import string

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'heroku_8qfx8bg5'
app.config['MONGO_URI'] = 'mongodb://admin:robin123@ds261077.mlab.com:61077/heroku_8qfx8bg5?retryWrites=false'

mongo = PyMongo(app)

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


@app.route('/orders')
def orders():
    return render_template("orders.html")


@app.route('/api/orders/poll')
def poll():
    cursor = mongo.db.orders.find({})
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
@app.route('/api/orders/add', methods=['POST'])
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
    mongo.db.orders.insert_one(order)
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
@app.route('/api/orders/remove', methods=['POST'])
def remove():
    mongo.db.orders.delete_many({"order_id": request.json["order_id"]})
    return "", 200


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)