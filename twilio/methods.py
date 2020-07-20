"""
This file contains supplementary methods that may be used in the main file.
"""


from twilio.twiml.messaging_response import MessagingResponse
from sample_menu import *
import pymongo
from pymongo import MongoClient


#setup database for all methods
cluster = MongoClient("mongodb+srv://isidonnelly:1234@cluster0.mgmae.mongodb.net/auto_order?retryWrites=true&w=majority")
db = cluster["auto_order"]
opc = db["order_process"]


"""
Sends a message.
Input: Message to be sent (string)
Returns: a message (string)
"""
def send_message(msg):
    resp = MessagingResponse()
    resp.message(msg)
    return str(resp)


"""
Finds the main item the customer wants.
Input: Message (string)
Returns: Main Item indicated (MainItem) OR error codes 
0 (the user indicated no main items)
1 (the user indicated more than 1 main item)
2 (the user indicated main items but the code somehow deleted all of them)
"""
def get_main_item(incoming_msg):

    #gets all the main items included in the user's input string
    possible_main_items = []
    for main_item in menu["main_items"]:
        for name in main_item["names_list"]:
            if name in incoming_msg:
                possible_main_items.append(main_item)
    
    #if the user did not indicate any main items, return error code 0 
    if len(possible_main_items) == 0:
        return 0

    #if the user only indicated on possible main item, return that main item
    if len(possible_main_items) == 1:
        return possible_main_items[0]
    
    #if the user indicated multiple main items
    if len(possible_main_items) > 1:

        #Perhaps one main item is "pizza" and another is "deep dish pizza". If the user orders "deep dish pizza" then the program will pick up on both.
        for possible_subitem in possible_main_items:
            for name1 in possible_subitem["names_list"]:
                for main_item in possible_main_items:
                    for name2 in main_item["names_list"]:
                        if possible_subitem != main_item:
                            if name1 in name2:
                                possible_main_items.remove(possible_subitem)

        #check if that narrowed list down to 1
        if len(possible_main_items) == 1:
            return possible_main_items[0]

        #Perhaps one of the main items is actually supposed to be a side. Like the person asks for a side of fries but fries is also a main item.
        for possible_side in possible_main_items:
            for main_item in possible_main_items:
                for side_list in main_item["adds_list"]:
                    for choice in side_list["choice_list"]:
                        if choice.name == possible_side["name"]:
                            possible_main_items.remove(possible_side)

        #check if that narrowed list down to 1
        if len(possible_main_items) == 1:
            return possible_main_items[0]

        #if there are still multiple possible items, return error code 1
        if len(possible_main_items) > 1:
            return 1

        #if there are somehow 0 items left return error code 2
        if len(possible_main_items) == 0:
            return 2

"""
Makes sure the current_item has all the sides filled out in accordance with min and max values.
Input: opc, phone number
Returns: question if a sublist is not filled out properly
"""
def assert_current(phone_number):

    #pull the current item from the db
    current_item = opc.find_one({"phone_number":phone_number})["current_item"]

    #iterate through sublist and make sure options match min/max requirements
    for sublist in current_item["main_item"]["adds_list"]:

        #gets how many items are in a certain sublist
        length = len(current_item[sublist["name"]])

        if length==0:
            return send_message(sublist["prompting_question"])

        if length<sublist["min_choices"]:
            return send_message("{q} (you must have a minimum of {min})".format(q=sublist["prompting_question"], min=sublist["min_choices"]))

        if length>sublist["max_choices"]:
            return send_message("{q} (you must have a maximum of {max})".format(q=sublist["prompting_question"], max=sublist["max_choices"]))

    #if none of the sublists had any issues
    return send_message("success!")


"""
Takes a message and find things in sublists and adds them to the current item.
Input: opc, phone number
"""
def fill_in_sublists(phone_number, msg):
    print("hi")
