"""
Sample menu in dictionary form.
"""


import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
db = cluster["0000"]
menu_collection = db["info"]


#Add On Choices
tonkotsu = {
    "name":"Tonkotsu",
    "names_list":["tonkotsu"],
    "add_price":2.0
}

tonkotsu_black = {
    "name":"Tonkotsu black",
    "names_list":["black"],
    "add_price":2.0
}

miso = {
    "name":"Miso",
    "names_list":["miso"],
    "add_price":0.0
}

spicy_miso = {
    "name": "Spicy miso",
    "names_list":["spicy"],
    "add_price":1.0
}

shoyu = {
    "name":"Shoyu",
    "names_list":["shoyu"],
    "add_price":0.0
}

shio = {
    "name":"Shio",
    "names_list":["shio"],
    "add_price":0.0
}

chashu = {
    "name":"Chashu",
    "names_list":["chashu", "pork belly"],
    "add_price":1.0
}

nitamago = {
    "name":"Nitamago",
    "names_list":["nitamago", "boiled egg"],
    "add_price":1.0
}

menma = {
    "name":"Menma",
    "names_list":["menma", "bamboo"],
    "add_price":0.50
}

kikurage = {
    "name":"Kikurage",
    "names_list":["kikurage", "mushroom"],
    "add_price":0.50
}

narutomaki = {
    "name":"Narutomaki",
    "names_list":["narutomaki", "fish cake"],
    "add_price":0.80
}

nori_seaweed = {
    "name":"Nori seaweed",
    "names_list":["nori seaweed", "nori", "seaweed"],
    "add_price":0.0
}

extra_toppings_none = {
    "name":"None",
    "names_list":["no toppings", "no extra toppings", "plain"],
    "add_price":0.0
}


#Add On Lists
ramen_flavors = {
    "name":"Flavors",
    "choice_list":[tonkotsu, tonkotsu_black, miso, spicy_miso, shoyu, shio],
    "min_choices":1,
    "max_choices":1,
    "prompting_question":"What flavor of ramen would you like?",
    "sublist_inceptions":[]
}

extra_ramen_toppings = {
    "name":"Extra toppings",
    "choice_list":[chashu, nitamago, menma, kikurage, narutomaki, nori_seaweed, extra_toppings_none],
    "min_choices":1,
    "max_choices":100,
    "prompting_question":"Which extra ramen toppings would you like?",
    "sublist_inceptions":[]
}

hirata_buns_flavors = {
    "name":"Ozu Hirata Buns",
    "choice_list":[bbq_pork_bun, chicken_karaage_bun, wasabi_mini_burger],
    "min_choices":1,
    "max_choices":100,
    "prompting_question":"Which Ozu Hirata Buns would you like?",
    "sublist_inceptions":[]
}

#Main Items
edamame = {
    "name":"Edamame",
    "names_list":["edamame"],
    "adds_list":[],
    "base_price":2.50
}

gyoza = {
    "name":"Gyoza",
    "names_list":["dumplings", "gyoza"],
    "adds_list":[],
    "base_price":2.75
}

takoyaki = {
    "name":"Takoyaki",
    "names_list":["takoyaki"],
    "adds_list":[],
    "base_price":3.0
}

chicken_wing = {
    "name":"Chicken wing",
    "names_list":["wings", "chicken wings", "chicken wing"],
    "adds_list":[],
    "base_price":3.0
}

salmon_share = {
    "name":"Salmon share",
    "names_list":["salmon share", "salmon"],
    "adds_list":[],
    "base_price":6.0
}

chicken_karaage = {
    "name":"Chicken karaage",
    "names_list":["chicken karaage", "karaage"],
    "adds_list":[],
    "base_price":4.0
}

ramen = {
    "name":"Ramen",
    "names_list":["ramen", "noodles", "raman"],
    "adds_list":[ramen_flavors, extra_ramen_toppings],
    "base_price":8.0
}

ozu_hirata_buns = {
    "name":"Ozu Hirata Buns",
    "names_list":["ozu hirata buns", "buns", "bun", "hirata bun"],
    "adds_list":[ozu_hirata_buns, burger_sides],
    "base_price":10.0
}

seared_salmon_plate = {
    "name":"Seared salmon plate",
    "names_list":["seared salmon plate", "salmon plate","salmon", "seared salmon"],
    "adds_list":[],
    "base_price":14.0
}

chicken_teriyaki = {
    "name":"Chicken teriyaki",
    "names_list":["chicken teriyaki", "chicken", "teriyaki", "teriyaki chicken"],
    "adds_list":[],
    "base_price":12.0
}

japanese_chashu_don = {
    "name":"Japanese Chashu Don",
    "names_list":["japanese chashu don", "chashu don", "chashu"],
    "adds_list":[],
    "base_price":12.0
}

short_rib_lover = {
    "name":"Short rib lover",
    "names_list":["short rib lover", "short ribs", "short rib"],
    "adds_list":[],
    "base_price":13.0
}

grilled_unagi_bowl = {
    "name":"Grilled unagi bowl",
    "names_list":["unagi", "unagi bowl", "grilled unagi bowl"],
    "adds_list":[],
    "base_price":14.0
}

ramune = {
    "name":"ramune",
    "names_list":["ramune"],
    "adds_list":[],
    "base_price":2.50
}

coca_cola = {
    "name":"Coca Cola",
    "names_list":["coke", "coca"],
    "adds_list":[],
    "base_price":1.0
}

sprite = {
    "name":"Sprite",
    "names_list":["sprite"],
    "adds_list":[],
    "base_price":1.0
}

green_tea = {
    "name":"Green tea",
    "names_list":["tea", "green tea"],
    "adds_list":[],
    "base_price":0.75
}

#Overall menu
menu = {
    "restaurant_name":"Ozu Ramen",
    "open_intro_message":"Welcome to Ozu Ramen! Here is our menu. What can we get for you?",
    "closed_intro_message":"Welcome to Ozu Ramen! Here is our menu. We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
    "main_items":[edamame, gyoza, takoyaki, chicken_wing, salmon_share, chicken_karaage, 
    ramen, ozu_hirata_buns, seared_salmon_plate, chicken_teriyaki, japanese_chashu_don, short_rib_lover, grilled_unagi_bowl, 
    ramune, coca_cola, sprite, green_tea]
}

menu_collection.delete_one({"_id":"menu"})
menu_collection.insert_one({"_id":"menu","main_items":[pizza, burger, coke, fries_main], "link":"https://uofi.box.com/s/ovex1fgqoutaf9ld57hoo8b69rzedzpm"})

menu_collection.delete_one({"_id":"info"})
menu_collection.insert_one({
    "_id":"info",
    "name":"Other Restaurant",
    "names":["other"],
    "open_intro":"Welcome to the Other Restaurant! Here is our menu. What can I get for you?",
    "closed_intro":"Welcome to the Other Restaurant! Here is our menu. We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
})