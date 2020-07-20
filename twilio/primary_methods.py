"""
This contains all the primary methods used in the code. After the section is identified, the main file calls a method from here.
"""

from sample_menu import *
from methods import *
import pymongo
from pymongo import MongoClient


#setup database
cluster = MongoClient("mongodb+srv://isidonnelly:1234@cluster0.mgmae.mongodb.net/auto_order?retryWrites=true&w=majority")
db = cluster["auto_order"]
opc = db["order_process"]


#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message(incoming_msg, phone_number):
    
    #initialize order object
    opc.insert_one({"phone_number":phone_number, "section":"ordering_process", "item_list":[], "method_of_getting_food":"pickup", "address":None, "comments":None})

    #send the restaurant's custom intro message
    return send_message(menu["open_intro_message"])


#triggered if the customer is in the middle of the ordering process
def ordering_process(incoming_msg, phone_number):

    #if the customer indicates they are done ordering
    if "finish" in incoming_msg:
        opc.update_one({"phone_number":phone_number}, {"$set":{"section":"finished_ordering"}})
        return send_message("Thank you for your order. It will be processed shortly.")
    
    #get the main item the customer ordered
    main_item_or_error_code = get_main_item(incoming_msg)

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
        item = {"main_item":main_item_or_error_code}
        for sublist in main_item_or_error_code["adds_list"]:
            item[sublist["name"]] = []
        opc.update_one({"phone_number":phone_number}, {"$set":{"current_item":item}})

        return assert_current(phone_number)
        """
        #make list of main items, update said list in db
        new_list = opc.find_one({"phone_number":phone_number})["item_list"]
        new_list.append(main_item_or_error_code)
        opc.update_one({"phone_number":phone_number}, {"$set":{"item_list":new_list}})

        #build message
        response = ""
        for item in new_list:
            response = response +"%s. " %item["name"]
        response = response+'What else would you like? If you would like to restart your order please text "restart." If that is all please text "finished."'
        return send_message(response)
        """
        


def finished_ordering(incoming_msg, phone_number):
    opc.delete_one({"phone_number":phone_number})
    return send_message("ur done")
    
    