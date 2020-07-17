"""
Sample menu in dictionary form.
"""


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
    "name":"Burger Toppings",
    "choice_list":[],
    "min_choices":0,
    "max_choices":100,
    "prompting_question":"What toppings would you like on your burger, if any?"
}

pizza_toppings = {
    "name":"Pizza Toppings",
    "choice_list":[],
    "min_choices":0,
    "max_choices":100,
    "prompting_question":"What toppings would you like on your pizza?"
}

pizza_sizes = {
    "name":"Pizza Sizes",
    "choice_list":[],
    "min_choices":1,
    "max_choices":1,
    "prompting_question":"What size pizza would you like?"
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
    "names_list":["burger, hamberder"],
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
    "main_items":[pizza, burger, coke],
    "open_intro_message":"Welcome to Cheesy Does It! Here is our menu. What can I get for you?",
    "closed_intro_message":"Welcome to Cheesy Does It! Here is our menu. We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True
}