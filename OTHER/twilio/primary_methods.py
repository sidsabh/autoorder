"""
This contains all the primary methods used in the code. After the section is identified, the main file calls a method from here.
"""

import g

import pymongo
from pymongo import MongoClient

from methods import *

import datetime


#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message():
    
    #if the restaurant is closed
    if not g.info["is_open"]:
        #delete the order
        g.delete_one(current_order())
        return send_message_and_menu(g.info["closed_intro"]+" Here is our menu.")
    
    #if the restaurant is open
    if g.info["is_open"]:

        #initialize response
        resp = g.info["open_intro"]+" Here is our menu."

        #if the restaurant offers delivery
        if g.info["offers_delivery"]:
            g.opc.update_one(current_order(), {"$set":{"section":"pickup_or_delivery"}})
            resp += " Is this order for pickup or delivery? "
        
        #if the restaurant does not offer delivery
        if not g.info["offers_delivery"]:
            g.opc.update_one(current_order(), {"$set":{"section":"ordering_process"}})
            resp += " This order will be for pickup."

        resp += '\n\nText "restart" at any time to restart the whole process.'

        #if there is an index
        if len(g.onc.find_one({"_id":g.to_num})["codes"]) > 1:
            resp += ' Text "index" at any time to cancel your order and return to the restaurant index.'

        return send_message_and_menu(resp)


#triggered if customer is indicating pickup or delivery
def pickup_or_delivery():
    
    #if the customer answers yes
    if is_similar("delivery"):
        g.opc.update_one(current_order(), {"$set":{"method_of_getting_food":"delivery"}})
        g.opc.update_one(current_order(), {"$set":{"section":"get_address"}})
        return send_message("What is your full address?")
    
    #if the customer answers no
    if is_similar("pickup"):
        g.opc.update_one(current_order(), {"$set":{"method_of_getting_food":"pickup"}})
        g.opc.update_one(current_order(), {"$set":{"section":"ordering_process"}})
        return send_message("What is the first item we can get for you?")
    
    #if the user did not indicate either of these
    else:
        return send_message('Sorry, we did not catch that. Please text "pickup" or "delivery". ')



#triggered if the user is typing in their address
def get_address():

    #if the user typed in something too short
    if len(g.msg) < 10:
        return send_message("This seems too short. Please text your full address.")

    #if the user supposedly typed in their address
    else:
        g.opc.update_one(current_order(), {"$set":{"address":g.msg}})
        g.opc.update_one(current_order(), {"$set":{"section":"ordering_process"}})
        return send_message("Thanks! What is the first item we can get for you?")



#triggered if the customer is in the middle of the ordering process
def ordering_process():

    #if the customer indicates they are done ordering
    if is_similar("finish"):

        #if the user didn't order anything
        if total_cost() == 0:
            return send_message("Sorry, your order must cost more than $0. Please order a main item.")

        #if the user did order something
        else:
            g.opc.update_one(current_order(), {"$set":{"section":"comments"}})
            return send_message('Please text anything you would like the chef to know about your order. If you have no comments just text "none".')
    
    #get the main item the customer ordered
    main_item_or_error_code = get_main_item()

    #if no specific main item was detected
    if main_item_or_error_code == 0:
        return send_message("It seems you did not order any of the main items on our menu. Please try again.")
    if main_item_or_error_code == 1:
        return send_message("It seems you have order too many main items. Please try again and only order one main item.")
    if main_item_or_error_code == 2:
        return send_message("It seems you have order too many main items. Please try again and only order one main item. ERROR CODE 2")
    
    #if a specific main item was detected
    else:

        #init a dictionary to insert in database, to be stored in temporary slot until all sublists are filled
        current_item = {"main_item":main_item_or_error_code}
        for sublist in main_item_or_error_code["adds_list"]:
            current_item[sublist["name"]] = []
        g.opc.update_one(current_order(), {"$set":{"current_item":current_item}})

        #try to fill in the sublists of the main item
        fill_in_sublists()

        return assert_current()
    


#if a sublist is in question
def sublist_in_q(sublist):

    fill_in_one_sublist(sublist)
    return(assert_current())


#if the user just texted their comments
def comments():

    if not is_similar("none"):
        g.opc.update_one(current_order(), {"$set":{"comments":g.msg}})
    
    g.opc.update_one(current_order(), {"$set":{"section":"finished_ordering"}})
    return checkout()

#if the user is done ordering, NEEDS WORK
def finished_ordering():
    g.opc.delete_one(current_order())

    return send_message("data cleared")
    
    