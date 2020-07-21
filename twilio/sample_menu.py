"""
Sample menu in dictionary form.
"""

import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://isidonnelly:1234@cluster0.mgmae.mongodb.net/auto_order?retryWrites=true&w=majority")
db = cluster["auto_order"]
menu_collection = db["menus"]


#Add On Choices
pizza_small = {
    "name":"Small",
    "names_list":["small"],
    "add_price":0.0
}

pizza_medium = {
    "name":"Medium",
    "names_list":["medium", "regular"],
    "add_price":2.0
}

pizza_large = {
    "name":"Large",
    "names_list":["large"],
    "add_price":4.0
}

tomatos = {
    "name":"Tomatos",
    "names_list":["tomato"],
    "add_price":0.5
}

lettuce = {
    "name":"Lettuce",
    "names_list":["lettuce"],
    "add_price":0.0
}

onion = {
    "name":"Onions",
    "names_list":["onion"],
    "add_price":1.0
}

pepperoni = {
    "name":"Pepperoni",
    "names_list":["pepperoni"],
    "add_price":2.0
}

mushroom = {
    "name":"Mushrooms",
    "names_list":["mushroom"],
    "add_price":1.0
}


#Add On Lists
burger_toppings = {
    "name":"Toppings",
    "choice_list":[onion, lettuce, tomatos],
    "min_choices":0,
    "max_choices":100,
    "prompting_question":"What toppings would you like on your burger, if any?",
    "sublist_inceptions":[]
}

pizza_toppings = {
    "name":"Toppings",
    "choice_list":[pepperoni, mushroom],
    "min_choices":0,
    "max_choices":100,
    "prompting_question":"What toppings would you like on your pizza?",
    "sublist_inceptions":[]
}

pizza_sizes = {
    "name":"Size",
    "choice_list":[pizza_large, pizza_medium, pizza_small],
    "min_choices":1,
    "max_choices":1,
    "prompting_question":"What size pizza would you like?",
    "sublist_inceptions":[]
}


#Main Items
pizza = {
    "name":"Pizza",
    "names_list":["pizza", "pie"],
    "adds_list":[pizza_sizes, pizza_toppings],
    "base_price":8.0
}

burger = {
    "name":"Hamburger",
    "names_list":["burger", "hamberder"],
    "adds_list":[burger_toppings],
    "base_price":10.0
}

coke = {
    "name":"Coke",
    "names_list":["coke","cola"],
    "adds_list":[],
    "base_price":1.5
}


#Overall menu
menu = {
    "restaurant_name":"Cheesy Does It",
    "open_intro_message":"Welcome to Cheesy Does It! Here is our menu. What can I get for you?",
    "closed_intro_message":"Welcome to Cheesy Does It! Here is our menu. We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
    "main_items":[pizza, burger, coke]
}

menu_collection.delete_one({"_id":0})
menu_collection.insert_one({"_id":0,"menu":menu})