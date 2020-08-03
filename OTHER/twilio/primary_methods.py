"""
This contains all the primary methods used in the code. After the section is identified, the main file calls a method from here.
"""

from settings import *
from essentials import *

from payment import *
from messaging import *
from order_processing import *

import datetime


#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message(msg):
    
    #if the restaurant is closed
    if not msg.rinfo["is_open"]:
        #delete the order
        OPC.delete_one(current_order(msg))
        return send_message_and_menu(msg, msg.rinfo["closed_intro"]+" Our menu will arrive momentarily.")
    
    #if the restaurant is open
    if msg.rinfo["is_open"]:

        #initialize response
        resp = msg.rinfo["open_intro"]+" Our menu will arrive momentarily."

        #if the restaurant offers delivery
        if msg.rinfo["offers_delivery"]:
            OPC.update_one(current_order(msg), {"$set":{"section":"pickup_or_delivery"}})
            resp += " Is this order for pickup or delivery? "
        
        #if the restaurant does not offer delivery
        if not msg.rinfo["offers_delivery"]:
            OPC.update_one(current_order(msg), {"$set":{"section":"ordering_process"}})
            resp += " This order will be for pickup."

        resp += '\n\nText "restart" at any time to restart the whole process.'

        #if there is an index
        if len(ONC.find_one({"_id":msg.to})["codes"]) > 1:
            resp += ' Text "index" at any time to cancel your order and return to the restaurant index.'

        #if this is the demo number
        if msg.to == "+12676276054":
            resp += "\n\nNote: this number is a ONLY A DEMO."

        return send_message_and_menu(msg, resp)


#triggered if customer is indicating pickup or delivery
def pickup_or_delivery(msg):
    
    #if the message indicates delivery
    if is_similar(msg, "delivery"):
        OPC.update_one(current_order(msg), {"$set":{"method_of_getting_food":"delivery"}})
        OPC.update_one(current_order(msg), {"$set":{"section":"get_address"}})
        return send_message("What is your full address?")
    
    #if the message indicates pickup
    if is_similar(msg, "pickup"):
        OPC.update_one(current_order(msg), {"$set":{"method_of_getting_food":"pickup"}})
        OPC.update_one(current_order(msg), {"$set":{"section":"ordering_process"}})
        return send_message("What is the first item we can get for you?")
    
    #if the user did not indicate either of these
    else:
        return send_message('Sorry, we did not catch that. Please text "pickup" or "delivery". ')



#triggered if the user is typing in their address
def get_address(msg):

    #if the user typed in something too short
    if len(msg.txt) < 10:
        return send_message("This seems too short. Please text your full address.")

    #if the user supposedly typed in their address
    else:
        OPC.update_one(current_order(msg), {"$set":{"address":msg.txt}})
        OPC.update_one(current_order(msg), {"$set":{"section":"ordering_process"}})
        return send_message("Thanks! What is the first item we can get for you?")



#triggered if the customer is in the middle of the ordering process
def ordering_process(msg):

    #if the customer indicates they are done ordering
    if is_similar(msg, "finish"):

        #if the user didn't order anything
        if subtotal(msg) < 0.5:
            return send_message("Sorry, your order must cost more than $0.50. Please order a main item.")

        #if the user did order something
        else:
            OPC.update_one(current_order(msg), {"$set":{"section":"comments"}})
            return send_message('Please text anything you would like the chef to know about your order. Text "none" if you have no comments.')
    
    #get the main item the customer ordered
    main_item_or_error_code = get_main_item(msg)

    #if no specific main item was detected
    if main_item_or_error_code == 0:
        return send_message("It seems you did not order any of the main items on our menu. Please try again.")
    if main_item_or_error_code == 1:
        return send_message("It seems you have order too many main items. Please try again and only order one main item.")
    if main_item_or_error_code == 2:
        return send_message("It seems you have order too many main items. Please try again and only order one main item.")
    
    #if a specific main item was detected
    else:

        #init a dictionary to insert in database, to be stored in temporary slot until all sublists are filled
        current_item = {"main_item":main_item_or_error_code}
        for sublist in main_item_or_error_code["adds_list"]:
            current_item[sublist["name"]] = []
        OPC.update_one(current_order(msg), {"$set":{"current_item":current_item}})

        #try to fill in the sublists of the main item
        fill_in_sublists(msg)

        #This function ensures all the sublists are filled out, and if not, messages the user appropriately
        return assert_current(msg)
    


#if a sublist is in question
def sublist_in_q(msg, sublist):

    fill_in_one_sublist(msg, sublist)
    return(assert_current(msg))


#if the user just texted their comments
def comments(msg):

    if not is_similar(msg, "none"):
        OPC.update_one(current_order(msg), {"$set":{"comments":msg.txt}})
    
    OPC.update_one(current_order(msg), {"$set":{"section":"finished_ordering"}})
    return checkout(msg)


#if the user is done ordering but the order has not been deleted yet
def finished_ordering(msg):

    return send_message("Please finish paying.")
    
    