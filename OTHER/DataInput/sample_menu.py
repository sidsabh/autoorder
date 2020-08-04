"""
Sample menu in dictionary form.
"""


import pymongo
from pymongo import MongoClient


#Add On Choices
pizza_small = {
    "name":"Small",
    "names_list":["small"],
    "add_price":0
}

pizza_medium = {
    "name":"Medium",
    "names_list":["medium", "regular"],
    "add_price":200
}

pizza_large = {
    "name":"Large",
    "names_list":["large"],
    "add_price":400
}

tomatos = {
    "name":"Tomatoes",
    "names_list":["tomato"],
    "add_price":50
}

lettuce = {
    "name":"Lettuce",
    "names_list":["lettuce"],
    "add_price":0
}

onion = {
    "name":"Onions",
    "names_list":["onion"],
    "add_price":100
}

fries = {
    "name": "French Fries",
    "names_list":["fries", "fry"],
    "add_price":300
}

pepperoni = {
    "name":"Pepperoni",
    "names_list":["pepperoni"],
    "add_price":175
}

mushroom = {
    "name":"Mushrooms",
    "names_list":["mushroom"],
    "add_price":155
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
    "base_price":800
}

burger = {
    "name":"Hamburger",
    "names_list":["burger", "hamberder"],
    "adds_list":[burger_toppings, burger_sides],
    "base_price":1000
}

coke = {
    "name":"Coke",
    "names_list":["coke","cola", "coca"],
    "adds_list":[],
    "base_price":150
}

fries_main = {
    "name":"French Fries",
    "names_list":["fries", "fry"],
    "adds_list":[],
    "base_price":50
}
'''
#Overall menu
menu_collection.insert_one({
    "_id":"0000",
    "name":"Cheesy Does It",
    "names":["cheesy"],
    "main_items": [pizza, burger, coke, fries_main],
    "link":"https://iili.io/dIAGcl.jpg",
    "open_intro":"Welcome to Cheesy Does It! Here is our menu. What can I get for you?",
    "closed_intro":"Welcome to Cheesy Does It! Here is our menu. We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
    "orders":[]
})
'''

cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
db = cluster["Deployment"]
menu_collection = db["restaurants"]

menu_collection.insert_one({
    "_id":"fries@gmail.com",
    "name":"50 Cent Friesaurant",
    "names":["fries"],
    "main_items": [pizza, burger, coke, fries_main],
    "link":"https://iili.io/dyBrEG.jpg",
    "open_intro":"Welcome to the Testaurant!",
    "closed_intro":"Welcome to the Testaurant! We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
    "orders":[],
    "tax":0.06
})
"""
menu_collection.insert_one({
    "_id":"cheesydoesit@gmail.com",
    "name":"Cheesy Does It",
    "names":["cheesy"],
    "main_items": [pizza, burger, coke, fries_main],
    "link":"https://iili.io/dyBrEG.jpg",
    "open_intro":"Welcome to Cheesy Does It!",
    "closed_intro":"Welcome to Cheesy Does It! We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":False,
    "is_open":True,
    "orders":[],
    "tax":0.06
})

menu_collection.insert_one({
    "_id":"otherrestaurant@gmail.com",
    "name":"Other Restaurant",
    "names":["other"],
    "main_items": [pizza, burger, coke, fries_main],
    "link":"https://iili.io/dyBrEG.jpg",
    "open_intro":"Welcome to the Other Restaurant!",
    "closed_intro":"Welcome to the Other Restaurant! We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":False,
    "is_open":False,
    "orders":[],
    "tax":0.06
})

"""