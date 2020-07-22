"""
This is the main code. Our program uses the flask web framework in combination with Twilio's API for sending sms messages
to enable text message ordering for restaurants.
"""


from flask import Flask, request, session
from sample_menu import *
from methods import *
import pymongo
from pymongo import MongoClient
from primary_methods import *


#setup database
cluster = MongoClient("mongodb+srv://isidonnelly:1234@cluster0.mgmae.mongodb.net/auto_order?retryWrites=true&w=majority")
db = cluster["auto_order"]
opc = db["order_process"]

#setup flask app
app = Flask(__name__)
app.config.from_object(__name__)

#entry point for when message comes in
@app.route("/sms", methods=['GET', 'POST'])
def main():
    
    #get the message that was sent and make it all lowercase
    incoming_msg = request.values.get('Text', None)
    incoming_msg = incoming_msg.lower()

    #get the phone number of the incoming msg
    phone_number = request.values.get('From', None)

    #get the phone number the message was sent to
    to_number = request.values.get('To', None)

    #get the order of the phone number
    order = opc.find_one({"phone_number":phone_number})

    #if the user wants to restart the order
    if incoming_msg == "restart":
        opc.delete_one({"phone_number":phone_number})
    
    #if this is the first message that the customer sends
    if order == None:
        return first_message(incoming_msg, phone_number, to_number)

    #if a sublist is being filled
    if order["sublist_in_q"]:
        return sublist_in_q(incoming_msg, phone_number, order["sublist_in_q"])

    #if the customer is in the ordering process
    if order["section"] == "ordering_process":
        return ordering_process(incoming_msg, phone_number)

    #if the customer just indicated they are finished ordering
    if order["section"] == "finished_ordering":
        return finished_ordering(incoming_msg, phone_number)




if __name__ == "__main__":
    app.run(debug=True)

