"""
This is the code for ordering once the program knows what restaurant the user is ordering from.
"""

import g

import pymongo
from pymongo import MongoClient

from methods import *
from primary_methods import *



def order_index():
    
    #get the order of the phone number
    order = g.opc.find_one({"from_num":g.from_num})

    #if the user wants to restart the order
    if g.msg == "restart":
        g.opc.delete_one({"from_num":g.from_num})
        order = None
    
    #if this is the first message that the customer sends
    if order == None:
        return first_message()

    #if a sublist is being filled
    if order["sublist_in_q"]:
        return sublist_in_q(order["sublist_in_q"])

    #if the customer is answering to pickup or delivery
    if order["section"] == "pickup_or_delivery":
        return pickup_or_delivery()

    #if the user needs to type in their address
    if order["section"] == "get_address":
        return get_address()

    #if the customer is in the ordering process
    if order["section"] == "ordering_process":
        return ordering_process()
        

    #if the customer just indicated they are finished ordering
    if order["section"] == "finished_ordering":
        return finished_ordering()


    #if none of these, then an error has occured
    else:
        return send_message("Sorry, an error has occured")



