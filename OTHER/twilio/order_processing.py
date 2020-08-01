"""
This file contains supplementary methods that may be used in the main file.
"""

from settings import *
from essentials import *

from messaging import *


"""
Finds the main item the customer wants.
Input: Message (string)
Returns: Main Item indicated (MainItem) OR error codes 
0 (the user indicated no main items)
1 (the user indicated more than 1 main item)
2 (the user indicated main items but the code somehow deleted all of them)
"""
def get_main_item(msg):

    #gets all the main items included in the user's input string
    possible_main_items = []
    for main_item in msg.rinfo["main_items"]:
        for name in main_item["names_list"]:
            if name in msg.txt:
                if main_item not in possible_main_items:
                    possible_main_items.append(main_item)
    
    #if the user did not indicate any main items, use the typo thing
    if len(possible_main_items) == 0:
        for main_item in msg.rinfo["main_items"]:
            for name in main_item["names_list"]:
                if is_similar(msg, name):
                    if main_item not in possible_main_items:
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
                                if possible_subitem in possible_main_items:
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
Input: OPC, phone number
Returns: question if a sublist is not filled out properly
"""
def assert_current(msg):
    
    #pull the current item from the db
    current_item = current_order(msg)["current_item"]

    #iterate through sublist and make sure options match min/max requirements
    for sublist in current_item["main_item"]["adds_list"]:

        #gets how many items are in a certain sublist
        length = len(current_item[sublist["name"]])

        #if both none and another option exist, delete the none option
        if length > 1:
            for subitem in current_item[sublist["name"]]:
                if subitem["name"] == "None":
                    current_item[sublist["name"]].remove(subitem)

        #if there are no items in a sublist (there must be at least one, even if the item is "none")
        if length==0:
            OPC.update_one(current_order(msg), {"$set":{"sublist_in_q":sublist}})
            OPC.update_one(current_order(msg), {"$set":{"section":"sublist"}})
            return send_message(sublist["prompting_question"]+your_options_are(sublist))

        #if the user indicated too many or too few items in a sublist
        if length<sublist["min_choices"] or length>sublist["max_choices"]:
            current_item[sublist["name"]] = []
            OPC.update_one(current_order(msg), {"$set":{"sublist_in_q":sublist}})
            OPC.update_one(current_order(msg), {"$set":{"current_item":current_item}})
            OPC.update_one(current_order(msg), {"$set":{"section":"sublist"}})
            return send_message("{q} (you must have a minimum of {min} and a maximum of {max})".format(q=sublist["prompting_question"], min=sublist["min_choices"], max=sublist["max_choices"])+your_options_are(sublist))
    

    #PROCEED IF NONE OF THE SUBLISTS HAD ISSUES

    #send user back to order process
    OPC.update_one(current_order(msg), {"$set":{"section":"ordering_process"}})

    #add the item to the item list
    item_list = current_order(msg)["item_list"]
    if item_list == None:
        item_list = []
    item_list.append(current_item)
    OPC.update_one(current_order(msg), {"$set":{"item_list":item_list}})

    #reset current_item and sublist_in_q
    OPC.update_one(current_order(msg), {"$set":{"current_item":None}})
    OPC.update_one(current_order(msg), {"$set":{"sublist_in_q":None}})

    #craft response
    resp = stringify_order(msg) + ' \n \nWhat is the next item I can get for you? Please text "finished" if that is it.'
    return send_message(resp)


"""
Takes a message and find things in sublists and adds them to the current item.
Input: phone number, msg
"""
def fill_in_sublists(msg):
    
    current_item = current_order(msg)["current_item"]
    
    for sublist in current_item["main_item"]["adds_list"]:
        
        for choice in sublist["choice_list"]:
            
            for name in choice["names_list"]:
                
                if is_similar(msg, name):
                    
                    current_item[sublist["name"]].append(choice)
                    OPC.update_one(current_order(msg), {"$set":{"current_item":current_item}})



"""
Takes a message and only fills in a specific sublist.
Input: phone number, msg, specific sublist
"""
def fill_in_one_sublist(msg, sublist):

    current_item = current_order(msg)["current_item"]

    for choice in sublist["choice_list"]:
            
        for name in choice["names_list"]:
                
            if is_similar(msg, name):
                    
                current_item[sublist["name"]].append(choice)
                OPC.update_one(current_order(msg), {"$set":{"current_item":current_item}})

    #if user did not specify any choices, use the none choice
    if len(current_item[sublist["name"]]) == 0:
        for choice in sublist["choice_list"]:
            if choice["name"] == "None":
                current_item[sublist["name"]].append(choice)
                OPC.update_one(current_order(msg), {"$set":{"current_item":current_item}})










