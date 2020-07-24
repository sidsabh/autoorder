"""
This contains all the primary methods used in the code. After the section is identified, the main file calls a method from here.
"""

import g

import pymongo
from pymongo import MongoClient

from methods import *



#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message():
    
    #initialize order object
    g.opc.insert_one({"from_num":g.from_num, "section":"ordering_process", "sublist_in_q":None, "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None})

    #send the restaurant's custom intro message
    return send_message(g.info["open_intro"])


#triggered if the customer is in the middle of the ordering process
def ordering_process():

    #if the customer indicates they are done ordering
    if "finish" in g.msg:
        g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"finished_ordering"}})
        return send_message("Thank you for your order. It will be processed shortly.")
    
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


def finished_ordering():
    g.opc.delete_one({"from_num":g.from_num})
    cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
    index_db = cluster["Index"]
    unc = index_db["user_numbers"]
    unc.update_one({"_id":"from_num"}, {"$set":{"current_order":None}})

    return send_message("data cleared")
    
    