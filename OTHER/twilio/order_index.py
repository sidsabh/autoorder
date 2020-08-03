"""
This is the code for ordering once the program knows what restaurant the user is ordering from. The current order is assumed to exist.
"""

from settings import *
from essentials import *

from messaging import *
from primary_methods import *



def order_index(msg):
    
    #get the order of the phone number
    order = OPC.find_one(current_order(msg))

    #if the user wants to restart the order
    if msg.txt == "restart":
        OPC.delete_one(current_order(msg))
        new_order = {"from_num":msg.fro, "to_num":msg.to, "code":order["code"], "timestamp":str(datetime.datetime.today()), "section":"first", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None, "payment_intent":None}
        order = new_order
        OPC.insert_one(order)

    #if a sublist is being filled
    if order["sublist_in_q"]:
        return sublist_in_q(msg, order["sublist_in_q"])

    #if this is the first message that the customer sends
    if order["section"] == "first":
        return first_message(msg)

    #if the customer is answering to pickup or delivery
    if order["section"] == "pickup_or_delivery":
        return pickup_or_delivery(msg)

    #if the user needs to type in their address
    if order["section"] == "get_address":
        return get_address(msg)

    #if the customer is in the ordering process
    if order["section"] == "ordering_process":
        return ordering_process(msg)
        
    #if the customer is entering comments
    if order["section"] == "comments":
        return comments(msg)

    #if the customer just indicated they are finished ordering
    if order["section"] == "finished_ordering":
        return finished_ordering(msg)


    #if none of these, then an error has occured
    else:
        return send_message("Sorry, an error has occured.")



