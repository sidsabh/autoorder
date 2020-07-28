"""
This contains all the primary methods used in the code. After the section is identified, the main file calls a method from here.
"""

import g

import pymongo
from pymongo import MongoClient

from methods import *


#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message():
    
    #if the restaurant is closed
    if not g.info["is_open"]:
        g.unc.update_one({"_id":g.from_num}, {"$set":{"current_order":None}})
        return send_message_and_menu(g.info["closed_intro"]+" Our menu is on its way.")
    
    #if the restaurant is open
    if g.info["is_open"]:

        #initialize order object
        g.opc.insert_one({"from_num":g.from_num, "section":"ordering_process", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None, "payment_intent":None})

        #if the restaurant offers delivery
        if g.info["offers_delivery"]:
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"pickup_or_delivery"}})
            return send_message_and_menu(g.info["open_intro"]+' Our menu is on its way. Is this order for pickup or delivery? \n\nText "restart" at any time to restart the whole process.')
        
        #if the restaurant does not offer delivery
        else:
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"ordering_process"}})
            return send_message_and_menu(g.info["open_intro"]+' This order will be for pickup. Our menu is on its way. What is the first item we can get for you? \n\nText "restart" at any time to restart the whole process.')




#triggered if customer is indicating pickup or delivery
def pickup_or_delivery():
    
    #if the customer answers yes
    if is_similar("delivery"):
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"method_of_getting_food":"delivery"}})
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"get_address"}})
        return send_message("What is your full address?")
    
    #if the customer answers no
    if is_similar("pickup"):
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"method_of_getting_food":"pickup"}})
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"ordering_process"}})
        return send_message("What is the first item we can get for you?")
    
    #if the user did not indicate either of these
    else:
        return send_message('Sorry, we did not catch that. Please text "pickup" or "delivery". ')



#triggered if the user is typing in their address
def get_address():

    if len(g.msg) < 10:
        return send_message("This seems too short. Please text your full address.")

    else:
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"address":g.msg}})
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"ordering_process"}})
        return send_message("Thanks! What is the first item we can get for you?")



#triggered if the customer is in the middle of the ordering process
def ordering_process():

    #if the customer indicates they are done ordering
    if is_similar("finish"):
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"comments"}})
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
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":current_item}})

        fill_in_sublists()

        return assert_current()
    


#if a sublist is in question
def sublist_in_q(sublist):

    fill_in_one_sublist(sublist)
    return(assert_current())


#if the user just texted their comments
def comments():

    if not is_similar("none"):
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"comments":g.msg}})
    
    g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"finished_ordering"}})
    return checkout()

def finished_ordering():
    g.opc.delete_one({"from_num":g.from_num})
    g.unc.update_one({"_id":g.from_num}, {"$set":{"current_order":None}})

    return send_message("data cleared")
    
    