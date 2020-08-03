"""
This file is for even more general methods. This file should not require any imports except global variables.
"""

from settings import *

from math import ceil

"""
Deals with typos. Returns true if the msg contains a word that matches to one letter off.
Input: The item name to match msg with
Returns: True or False
"""
def is_similar(msg, Word):

    Same = False

    for Sen_Word in msg.txt.split(" "):
        if Word in Sen_Word: Same = True
        
        elif len(Sen_Word) == len(Word)+1:
            Left_Count=Right_Count=0
            for i, x in zip(Sen_Word, Word):
                if i == x: Left_Count += 1
                else: break
                
            Letters_Left = min(len(Sen_Word), len(Word))-Left_Count
            for i, x in zip(Sen_Word[::-1], Word[::-1]):
                if Letters_Left - Right_Count > 0 and i == x: Right_Count += 1
                else: break
            if Left_Count + Right_Count == len(Word): Same = True


        elif len(Sen_Word) == len(Word):
            Left_Count=Right_Count=0
            for i, x in zip(Sen_Word, Word):
                if i == x: Left_Count += 1
                else: break
                
            Letters_Left = min(len(Sen_Word), len(Word))-Left_Count
            for i, x in zip(Sen_Word[::-1], Word[::-1]):
                if Letters_Left - Right_Count > 0 and i == x: Right_Count += 1
                else: break
            if Left_Count + Right_Count == len(Word)-1: Same = True


        elif len(Word) == len(Sen_Word)+1:

            Left_Count=Right_Count=0
            for i, x in zip(Word, Sen_Word):
                 
                if i == x: Left_Count += 1
                else: break
            
            Letters_Left = min(len(Word), len(Sen_Word))-Left_Count
            for i, x in zip(Word[::-1], Sen_Word[::-1]):
                if Letters_Left - Right_Count > 0 and i == x: Right_Count += 1
                else: break
            if Left_Count + Right_Count == len(Sen_Word): Same = True


    return Same


"""
Turns an item the customer ordered into a string to be repeated back to them.
Input: item (current_item)
Returns: A string, example: "1x Pizza[$8] (Size: Medium[+$2]. Toppings: Pepperoni[+$1], Mushroom[+$0.5], Onion[+$1].)."
"""
def stringify_order(msg):
     
    resp = "YOUR ORDER: "
    item_list = current_order(msg)["item_list"]

    for item in item_list:

        item_str = "\n\n1x {main_name} {main_price} ".format(main_name=item["main_item"]["name"], main_price=pricify(item["main_item"]["base_price"]))

        if len(item["main_item"]["adds_list"]) > 0:

            item_str += "\n"

            for sublist in item["main_item"]["adds_list"]:

                item_str += "{sub_name}: ".format(sub_name=sublist["name"])

                for subitem in item[sublist["name"]]:

                    item_str += "{name} +{price}".format(name=subitem["name"], price=pricify(subitem["add_price"]))
                    if subitem == item[sublist["name"]][-1]:
                        item_str += ". "
                    else:
                        item_str += ", "

            item_str = item_str[:-1] 

        resp += item_str

    resp += " \n\nSUBTOTAL: {cost}".format(cost=pricify(subtotal(msg)))
    resp += "\nTAX: {tax}".format(tax=pricify(tax(msg)))
    resp += "\nTOTAL COST: {total}".format(total=pricify(subtotal(msg)+tax(msg)))

    return resp


"""
Totals the cost of all the items in the order.
Returns: Float of total order cost
"""
def subtotal(msg):

    item_list = current_order(msg)["item_list"]
    cost = 0

    for item in item_list:
        cost += item["main_item"]["base_price"]
        for sublist in item["main_item"]["adds_list"]:
            for subitem in item[sublist["name"]]:
                cost += subitem["add_price"]

    return cost


"""
Get the tax of the total cost.
Returns: Amount of tax based on order total and specific restaurant tax rate.
"""
def tax(msg):

    #get subtotal, tax rate
    sub = subtotal(msg)
    rate = msg.rinfo["tax"]
    #amount of money going to restaurant based on stripe commission and transaction fees and our transaction fee
    restaurant_total = 0.971*sub - 0.3 - 0.2
    #tax is 2.9% more than the tax rate because of stripe's commission
    tax = rate*restaurant_total*1.029
    tax_rounded = ceil(tax * (10**2)) / float(10**2)
    return tax_rounded



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


"""
Finds the current version of the current item.
"""
def current_order(msg):
    return OPC.find_one({"from_num":msg.fro, "to_num":msg.to})

