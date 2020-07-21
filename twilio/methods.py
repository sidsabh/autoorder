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
            opc.update_one({"phone_number":phone_number}, {"$set":{"section":"sublist"}})
            return send_message(sublist["prompting_question"])

        if length<sublist["min_choices"]:
            current_item[sublist["name"]] = []
            opc.update_one({"phone_number":phone_number}, {"$set":{"current_item":current_item}})
            opc.update_one({"phone_number":phone_number}, {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min=sublist["min_choices"], max=sublist["max_choices"]))

        if length>sublist["max_choices"]:
            current_item[sublist["name"]] = []
            opc.update_one({"phone_number":phone_number}, {"$set":{"current_item":current_item}})
            opc.update_one({"phone_number":phone_number}, {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min = sublist["min_choices"], max=sublist["max_choices"]))

    #if none of the sublists had any issues
    opc.update_one({"phone_number":phone_number}, {"$set":{"section":"ordering_process"}})
    resp = "YOUR ORDER: "
    
    item_list = opc.find_one({"phone_number":phone_number})["item_list"]
    if item_list == None:
        item_list = []
    item_list.append(current_item)
    opc.update_one({"phone_number":phone_number}, {"$set":{"item_list":item_list}})

    for item in item_list:
        resp += stringify(item)

    resp += ' \n \nWhat is the next item I can get for you? If you are done text "finished". If you would like to restart text "restart".'
    return send_message(resp)


"""
Takes a message and find things in sublists and adds them to the current item.
Input: opc, phone number
"""
def fill_in_sublists(phone_number, incoming_msg):
    
    current_item = opc.find_one({"phone_number":phone_number})["current_item"]
    
    for sublist in current_item["main_item"]["adds_list"]:
        
        for choice in sublist["choice_list"]:
            
            for name in choice["names_list"]:
                
                if name in incoming_msg:
                    
                    current_item[sublist["name"]].append(choice)
                    opc.update_one({"phone_number":phone_number}, {"$set":{"current_item":current_item}})



"""
Turns an item the customer ordered into a string to be repeated back to them.
Input: item (current_item)
Returns: A string, example: "1x Pizza[$8] (Size: Medium[+$2]. Toppings: Pepperoni[+$1], Mushroom[+$0.5], Onion[+$1].)."
"""
def stringify(item):
     
    string = "1x {main_name}[${main_price}] ".format(main_name=item["main_item"]["name"], main_price=item["main_item"]["base_price"])

    if len(item["main_item"]["adds_list"]) > 0:

        string += "("

        for sublist in item["main_item"]["adds_list"]:

            string += "{sub_name}: ".format(sub_name=sublist["name"])

            for subitem in item[sublist["name"]]:

                string += "{name}[+${price}]".format(name=subitem["name"], price=subitem["add_price"])
                if subitem == item[sublist["name"]][-1]:
                    string += ". "
                else:
                    string += ", "

        string = string[:-1]
        string += ")" 

    string += "."

    return string


"""

"""

def total_cost():
