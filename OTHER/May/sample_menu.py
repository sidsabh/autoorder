"""
Sample menu in dictionary form.
"""


import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
db = cluster["Info"]
collection = db["restaurants"]


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
    "name":"Nori Seaweed",
    "names_list":["nori", "seaweed"],
    "add_price":0.0
}

extra_toppings_none = {
    "name":"None",
    "names_list":["no toppings", "no extra toppings", "plain"],
    "add_price":0.0
}

bbq_pork_bun = {
    "name":"BBQ Pork Bun",
    "names_list":["nori", "seaweed"],
    "add_price":0.0
}

chicken_karaage_bun = {
    "name":"Chicken Karaage Bun",
    "names_list":["nori", "seaweed"],
    "add_price":0.0
}

wasabi_mini_burger = {
    "name":"Wasabi Mini Burger",
    "names_list":["nori", "seaweed"],
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
    "name":"Chicken Wing",
    "names_list":["wings"],
    "adds_list":[],
    "base_price":3.0
}

salmon_share = {
    "name":"Salmon Share",
    "names_list":["salmon share"],
    "adds_list":[],
    "base_price":6.0
}

chicken_karaage = {
    "name":"Chicken Karaage",
    "names_list":["karaage"],
    "adds_list":[],
    "base_price":4.0
}

ramen = {
    "name":"Ramen",
    "names_list":["ramen", "noodles"],
    "adds_list":[ramen_flavors, extra_ramen_toppings],
    "base_price":8.0
}

ozu_hirata_buns = {
    "name":"Ozu Hirata Buns",
    "names_list":["buns"],
    "adds_list":[hirata_buns_flavors],
    "base_price":10.0
}

seared_salmon_plate = {
    "name":"Seared Salmon Plate",
    "names_list":["seared salmon", "salmon plate"],
    "adds_list":[],
    "base_price":14.0
}

chicken_teriyaki = {
    "name":"Chicken Teriyaki",
    "names_list":["chicken", "teriyaki"],
    "adds_list":[],
    "base_price":12.0
}

japanese_chashu_don = {
    "name":"Japanese Chashu Don",
    "names_list":["chashu"],
    "adds_list":[],
    "base_price":12.0
}

short_rib_lover = {
    "name":"Short Rib Lover",
    "names_list":["short rib"],
    "adds_list":[],
    "base_price":13.0
}

grilled_unagi_bowl = {
    "name":"Grilled Unagi Bowl",
    "names_list":["unagi"],
    "adds_list":[],
    "base_price":14.0
}

ramune = {
    "name":"Ramune",
    "names_list":["ramune"],
    "adds_list":[],
    "base_price":2.50
}

coca_cola = {
    "name":"Coca Cola",
    "names_list":["coke", "coca", "cola"],
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
    "names_list":["tea"],
    "adds_list":[],
    "base_price":0.75
}

#Overall menu
menu = {
    "_id":"0003",
    "name":"Ozu Ramen",
    "names":["ozu", "ramen"],
    "main_items":[edamame, gyoza, takoyaki, chicken_wing, salmon_share, chicken_karaage, 
    ramen, ozu_hirata_buns, seared_salmon_plate, chicken_teriyaki, japanese_chashu_don, short_rib_lover, grilled_unagi_bowl, 
    ramune, coca_cola, sprite, green_tea],
    "link":"https://iili.io/d7Hc8u.jpg",
    "open_intro":"Welcome to Ozu Ramen!",
    "closed_intro":"Welcome to Ozu Ramen! We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
    "orders":[]
}


collection.insert_one(menu)