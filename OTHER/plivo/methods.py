"""
This file contains supplementary methods that may be used in the main file.
"""

import g
from more_methods import *

import plivo
from plivo import plivoxml

import pymongo
from pymongo import MongoClient

import stripe
stripe.api_key = 'sk_test_51H7n9PDTJ2YcvBWss1pfBvdXC70jEZ8wV4vpVhF0dViTlNRc9kRigRMJfJSoi6lYCJclszW3Ejx9qDXcCWwvtWyF00KHSY6yyV'


from flask import Flask, request, make_response, Response, url_for


def send_message(resp):
    response = plivoxml.ResponseElement()
    response.add(
        plivoxml.MessageElement(
            resp,
            src=g.to_num,  
            dst=g.from_num))
    return Response(response.to_string(), mimetype='application/xml')


def send_message_and_menu(resp):

    client = plivo.RestClient("MANTRLMJBHZTFKN2M5NW", "MTFiNDljZTkwNzQ1M2Q2ZDFjNGNiYTVmZTJiYmFh")

    response = client.messages.create(
        src=g.to_num,
        dst=g.from_num,
        text="",
        media_urls=[g.menu["link"]],
        type_='mms'
        )

    response2 = plivoxml.ResponseElement()
    response2.add(
        plivoxml.MessageElement(
            resp,
            src=g.to_num,  
            dst=g.from_num))
    return Response(response2.to_string(), mimetype='application/xml')



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
    for main_item in g.menu["main_items"]:
        for name in main_item["names_list"]:
            if name in g.msg:
                possible_main_items.append(main_item)
    
    #if the user did not indicate any main items, use the typo thing
    if len(possible_main_items) == 0:
        for main_item in g.menu["main_items"]:
            for name in main_item["names_list"]:
                if is_similar(name):
                    possible_main_items.append(main_item)

    #if that still does not work, return error code 0
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
Input: g.opc, phone number
Returns: question if a sublist is not filled out properly
"""
def assert_current():
    
    #pull the current item from the db
    current_item = g.opc.find_one({"from_num":g.from_num})["current_item"]

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
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"sublist_in_q":sublist}})
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"sublist"}})
            return send_message(sublist["prompting_question"]+your_options_are(sublist))

        if length<sublist["min_choices"]:
            current_item[sublist["name"]] = []
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"sublist_in_q":sublist}})
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":current_item}})
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min=sublist["min_choices"], max=sublist["max_choices"])+your_options_are(sublist))

        if length>sublist["max_choices"]:
            current_item[sublist["name"]] = []
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"sublist_in_q":sublist}})
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":current_item}})
            g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min = sublist["min_choices"], max=sublist["max_choices"])+your_options_are(sublist))

    #if none of the sublists had any issues
    g.opc.update_one({"from_num":g.from_num}, {"$set":{"section":"ordering_process"}})
    resp = ""
    item_list = g.opc.find_one({"from_num":g.from_num})["item_list"]
    if item_list == None:
        item_list = []
    item_list.append(current_item)
    g.opc.update_one({"from_num":g.from_num}, {"$set":{"item_list":item_list}})

    resp += stringify_order()
    resp += ' \n \nWhat is the next item I can get for you? If you are done text "finished"'

    g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":None}})
    g.opc.update_one({"from_num":g.from_num}, {"$set":{"sublist_in_q":None}})

    return send_message(resp)


"""
Takes a message and find things in sublists and adds them to the current item.
Input: phone number, msg
"""
def fill_in_sublists():
    
    current_item = g.opc.find_one({"from_num":g.from_num})["current_item"]
    
    for sublist in current_item["main_item"]["adds_list"]:
        
        for choice in sublist["choice_list"]:
            
            for name in choice["names_list"]:
                
                if is_similar(name):
                    
                    current_item[sublist["name"]].append(choice)
                    g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":current_item}})



"""
Takes a message and only fills in a specific sublist.
Input: phone number, msg, specific sublist
"""
def fill_in_one_sublist(sublist):

    current_item = g.opc.find_one({"from_num":g.from_num})["current_item"]

    for choice in sublist["choice_list"]:
            
        for name in choice["names_list"]:
                
            if is_similar(name):
                    
                current_item[sublist["name"]].append(choice)
                g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":current_item}})

    #if user did not specify any choices, use the none choice
    if len(current_item[sublist["name"]]) == 0:
        for choice in sublist["choice_list"]:
            if choice["name"] == "None":
                current_item[sublist["name"]].append(choice)
                g.opc.update_one({"from_num":g.from_num}, {"$set":{"current_item":current_item}})


"""
Sends the user a link to checkout.
"""
def checkout():
  
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[{
            
            'price_data': {
                'unit_amount': int(total_cost()*100),
                'currency': 'usd',
                'product': 'prod_HifPkxqBklYeQl',
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='https://www.google.com',
        cancel_url='https://www.google.com',
    )

   
    return send_message("localhost:5000/{id}".format(id=session.id))








