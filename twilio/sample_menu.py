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
    "name":"Tomatoes",
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

fries = {
    "name": "French Fries",
    "names_list":["fries", "fry"],
    "add_price":3.0
}

pepperoni = {
    "name":"Pepperoni",
    "names_list":["pepperoni"],
    "add_price":1.75
}

mushroom = {
    "name":"Mushrooms",
    "names_list":["mushroom"],
    "add_price":1.55
}

burger_toppings_none = {
    "name":"None",
    "names_list":["plain", "no topping"],
    "add_price":0
}

burger_sides_none = {
    "name":"None",
    "names_list":["no sides"],
    "add_price":0
}

pizza_toppings_none = {
    "name":"None",
    "names_list":["no toppings", "cheese", "plain"],
    "add_price":0
}


#Add On Lists
burger_toppings = {
    "name":"Toppings",
    "choice_list":[onion, lettuce, tomatos, burger_toppings_none],
    "min_choices":1,
    "max_choices":100,
    "prompting_question":"What toppings would you like on your burger, if any?",
    "sublist_inceptions":[]
}

burger_sides = {
    "name":"Sides",
    "choice_list":[fries, burger_sides_none],
    "min_choices":1,
    "max_choices":100,
    "prompting_question":"What sides would you like with your burger, if any?",
    "sublist_inceptions":[]
}

pizza_toppings = {
    "name":"Toppings",
    "choice_list":[pepperoni, mushroom, pizza_toppings_none],
    "min_choices":1,
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
    "adds_list":[burger_toppings, burger_sides],
    "base_price":10.0
}

coke = {
    "name":"Coke",
    "names_list":["coke","cola"],
    "adds_list":[],
    "base_price":1.5
}

fries = {
    "name":"French Fries",
    "names_list":["fries", "fry"],
    "adds_list":[],
    "base_price":5.0
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
    "main_items":[pizza, burger, coke, fries]
}

menu_collection.delete_one({"_id":0})
menu_collection.insert_one({"_id":0,"menu":menu})