"""
This file contains supplementary methods that may be used in the main file.
"""


#from plivo import plivoxml
import g
from twilio.twiml.messaging_response import MessagingResponse
from sample_menu import *
import pymongo
from pymongo import MongoClient
from flask import Flask, request, make_response, Response
#from app import *
#from primary_methods import *


#setup database for all methods
cluster = MongoClient("mongodb+srv://isidonnelly:1234@cluster0.mgmae.mongodb.net/auto_order?retryWrites=true&w=majority")
db = cluster["auto_order"]
opc = db["order_process"]


"""
Sends a message.
Input: Message to be sent (string)
Returns: a message (string)
"""
def send_message(resp):
    response = MessagingResponse()
    response.message(resp)
    return str(response)

'''
def send_message(resp):
    response = plivoxml.ResponseElement()
    response.add(
        plivoxml.MessageElement(
            resp,
            src=to_num,  
            dst=from_num))
    return Response(response.to_string(), mimetype='application/xml')
'''


"""
Finds the main item the customer wants.
Input: Message (string)
Returns: Main Item indicated (MainItem) OR error codes 
0 (the user indicated no main items)
1 (the user indicated more than 1 main item)
2 (the user indicated main items but the code somehow deleted all of them)
"""
def get_main_item():

    #gets all the main items included in the user's input string
    possible_main_items = []
    for main_item in menu["main_items"]:
        for name in main_item["names_list"]:
            if name in msg:
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
                        if choice["name"] == possible_side["name"]:
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
def assert_current():

    #pull the current item from the db
    current_item = opc.find_one({"from_num":from_num})["current_item"]

    #iterate through sublist and make sure options match min/max requirements
    for sublist in current_item["main_item"]["adds_list"]:

        #gets how many items are in a certain sublist
        length = len(current_item[sublist["name"]])

        #if both none and another option exist, delete the none option
        if length > 1:
            for subitem in current_item[sublist["name"]]:
                if subitem["name"] == "None":
                    current_item[sublist["name"]].remove(subitem)

        if length==0:
            opc.update_one({"from_num":from_num}, {"$set":{"sublist_in_q":sublist}})
            opc.update_one({"from_num":from_num}, {"$set":{"section":"sublist"}})
            return send_message(sublist["prompting_question"]+your_options_are(sublist))

        if length<sublist["min_choices"]:
            current_item[sublist["name"]] = []
            opc.update_one({"from_num":from_num}, {"$set":{"sublist_in_q":sublist}})
            opc.update_one({"from_num":from_num}, {"$set":{"current_item":current_item}})
            opc.update_one({"from_num":from_num}, {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min=sublist["min_choices"], max=sublist["max_choices"])+your_options_are(sublist))

        if length>sublist["max_choices"]:
            current_item[sublist["name"]] = []
            opc.update_one({"from_num":from_num}, {"$set":{"sublist_in_q":sublist}})
            opc.update_one({"from_num":from_num}, {"$set":{"current_item":current_item}})
            opc.update_one({"from_num":from_num}, {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min = sublist["min_choices"], max=sublist["max_choices"])+your_options_are(sublist))

    #if none of the sublists had any issues
    opc.update_one({"from_num":from_num}, {"$set":{"section":"ordering_process"}})
    resp = ""
    item_list = opc.find_one({"from_num":from_num})["item_list"]
    if item_list == None:
        item_list = []
    item_list.append(current_item)
    opc.update_one({"from_num":from_num}, {"$set":{"item_list":item_list}})

    resp += stringify_order()
    resp += ' \n \nWhat is the next item I can get for you? If you are done text "finished". If you would like to restart text "restart".'

    opc.update_one({"from_num":from_num}, {"$set":{"current_item":None}})
    opc.update_one({"from_num":from_num}, {"$set":{"sublist_in_q":None}})

    return send_message(resp)


"""
Takes a message and find things in sublists and adds them to the current item.
Input: phone number, msg
"""
def fill_in_sublists():
    
    current_item = opc.find_one({"from_num":from_num})["current_item"]
    
    for sublist in current_item["main_item"]["adds_list"]:
        
        for choice in sublist["choice_list"]:
            
            for name in choice["names_list"]:
                
                if name in msg:
                    
                    current_item[sublist["name"]].append(choice)
                    opc.update_one({"from_num":from_num}, {"$set":{"current_item":current_item}})



"""
Takes a message and only fills in a specific sublist.
Input: phone number, msg, specific sublist
"""
def fill_in_one_sublist(sublist):

    current_item = opc.find_one({"from_num":from_num})["current_item"]

    for choice in sublist["choice_list"]:
            
        for name in choice["names_list"]:
                
            if name in msg:
                    
                current_item[sublist["name"]].append(choice)
                opc.update_one({"from_num":from_num}, {"$set":{"current_item":current_item}})

    #if user did not specify any choices, use the none choice
    if len(current_item[sublist["name"]]) == 0:
        for choice in sublist["choice_list"]:
            if choice["name"] == "None":
                current_item[sublist["name"]].append(choice)
                opc.update_one({"from_num":from_num}, {"$set":{"current_item":current_item}})




"""
Turns an item the customer ordered into a string to be repeated back to them.
Input: item (current_item)
Returns: A string, example: "1x Pizza[$8] (Size: Medium[+$2]. Toppings: Pepperoni[+$1], Mushroom[+$0.5], Onion[+$1].)."
"""
def stringify_order():
     
    resp = "YOUR ORDER: "
    item_list = opc.find_one({"from_num":from_num})["item_list"]

    for item in item_list:

        item_str = "\n\n1x {main_name} {main_price} ".format(main_name=item["main_item"]["name"], main_price=pricify(item["main_item"]["base_price"]))

        if len(item["main_item"]["adds_list"]) > 0:

            item_str += "\n"
            #item_str += "("

            for sublist in item["main_item"]["adds_list"]:

                item_str += "{sub_name}: ".format(sub_name=sublist["name"])

                for subitem in item[sublist["name"]]:

                    item_str += "{name} +{price}".format(name=subitem["name"], price=pricify(subitem["add_price"]))
                    if subitem == item[sublist["name"]][-1]:
                        item_str += ". "
                    else:
                        item_str += ", "

            item_str = item_str[:-1]
            #item_str += ")" 

        resp += item_str

    resp += " \n\nTOTAL COST: {cost}".format(cost=pricify(total_cost()))

    return resp



"""
Totals the cost of all the items in the order.
Returns: Float of total order cost
"""
def total_cost():

    item_list = opc.find_one({"from_num":from_num})["item_list"]
    cost = 0

    for item in item_list:
        cost += item["main_item"]["base_price"]
        for sublist in item["main_item"]["adds_list"]:
            for subitem in item[sublist["name"]]:
                cost += subitem["add_price"]

    return cost



"""
Makes a string like: "Your options are: pepperoni mushroom onion etc." for a sublist
Input: A sublist
Returns: string
"""
def your_options_are(sublist):

    resp = "\n\nYour options are:"
    for subitem in sublist["choice_list"]:
        resp += "\n{item_name}".format(item_name=subitem["name"])
        resp += " (+{priced})".format(priced=pricify(subitem["add_price"]))

    return resp



"""
Makes prices look nice. (8.0 -> $8)
Input: a float
Output: a string
"""
def pricify(price):
    if float(price).is_integer():
        price = int(price)
        resp = "${price}".format(price=price)
    elif (price/0.1).is_integer():
        resp = "${price}0".format(price=price)
    else:
        resp = "${price}".format(price=price)

    return resp



