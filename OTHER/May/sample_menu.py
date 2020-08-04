"""
Sample menu in dictionary form.
"""


import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
db = cluster["Development"]
collection = db["restaurants"]


#Add On Choices
chashu = {
    "name":"Chashu",
    "names_list":["chashu", "pork belly"],
    "add_price":100
}

nitamago = {
    "name":"Nitamago",
    "names_list":["nitamago", "boiled egg"],
    "add_price":100
}

menma = {
    "name":"Menma",
    "names_list":["menma", "bamboo"],
    "add_price":50
}

kikurage = {
    "name":"Kikurage",
    "names_list":["kikurage", "mushroom"],
    "add_price":50
}

narutomaki = {
    "name":"Narutomaki",
    "names_list":["narutomaki", "fish cake"],
    "add_price":80
}

nori_seaweed = {
    "name":"Nori Seaweed",
    "names_list":["nori", "seaweed"],
    "add_price":0
}

butter = {
    "name":"Butter",
    "names_list":["butter"],
    "add_price":0
}

corn = {
    "name":"Corn",
    "names_list":["corn"],
    "add_price":0
}

extra_toppings_none = {
    "name":"None",
    "names_list":["no extra toppings", "plain"],
    "add_price":0
}

#Add On Lists
extra_ramen_toppings = {
    "name":"Extra toppings",
    "choice_list":[chashu, nitamago, menma, kikurage, narutomaki, nori_seaweed, butter, corn, extra_toppings_none],
    "min_choices":1,
    "max_choices":100,
    "prompting_question":"Which extra ramen toppings would you like?",
    "sublist_inceptions":[]
}

#Main Items
edamame = {
    "name":"Edamame",
    "names_list":["edamame"],
    "adds_list":[],
    "base_price":250
}

gyoza = {
    "name":"Gyoza",
    "names_list":["dumplings", "gyoza"],
    "adds_list":[],
    "base_price":275
}

takoyaki = {
    "name":"Takoyaki",
    "names_list":["takoyaki"],
    "adds_list":[],
    "base_price":300
}

chicken_wing = {
    "name":"Chicken Wing",
    "names_list":["wings"],
    "adds_list":[],
    "base_price":300
}

salmon_share = {
    "name":"Salmon Share",
    "names_list":["salmon share"],
    "adds_list":[],
    "base_price":600
}

chicken_karaage = {
    "name":"Chicken Karaage",
    "names_list":["karaage"],
    "adds_list":[],
    "base_price":400
}

tonkotsu_ramen = {
    "name":"Tonkotsu Ramen",
    "names_list":["tonkotsu"],
    "adds_list":[extra_ramen_toppings],
    "base_price":1200
}

tonkotsu_black_ramen = {
    "name":"Tonkotsu Black Ramen",
    "names_list":["tonkotsu black", "black tonkotsu"],
    "adds_list":[extra_ramen_toppings],
    "base_price":1200
}

miso_ramen = {
    "name":"Miso Ramen",
    "names_list":["miso"],
    "adds_list":[extra_ramen_toppings],
    "base_price":1000
}

spicy_miso_ramen = {
    "name":"Spicy Miso Ramen",
    "names_list":["spicy miso", "miso spicy"],
    "adds_list":[extra_ramen_toppings],
    "base_price":1000
}

shoyu_ramen = {
    "name":"Shoyu Ramen",
    "names_list":["shoyu"],
    "adds_list":[extra_ramen_toppings],
    "base_price":1100
}

shio_ramen = {
    "name":"Shio Ramen",
    "names_list":["shio"],
    "adds_list":[extra_ramen_toppings],
    "base_price":1100
}

bbq_pork_bun = {
    "name":"BBQ Pork Bun",
    "names_list":["bbq pork"],
    "adds_list":[],
    "base_price":300
}

chicken_karaage_bun = {
    "name":"Chicken Karaage Bun",
    "names_list":["chicken karaage"],
    "adds_list":[],
    "base_price":300
}

wasabi_mini_burger = {
    "name":"Wasabi Mini Burger",
    "names_list":["wasabi mini burger"],
    "adds_list":[],
    "base_price":300
}

seared_salmon_plate = {
    "name":"Seared Salmon Plate",
    "names_list":["seared salmon", "salmon plate"],
    "adds_list":[],
    "base_price":1400
}

chicken_teriyaki = {
    "name":"Chicken Teriyaki",
    "names_list":["chicken", "teriyaki"],
    "adds_list":[],
    "base_price":1200
}

japanese_chashu_don = {
    "name":"Japanese Chashu Don",
    "names_list":["chashu"],
    "adds_list":[],
    "base_price":1200
}

short_rib_lover = {
    "name":"Short Rib Lover",
    "names_list":["short rib"],
    "adds_list":[],
    "base_price":1300
}

grilled_unagi_bowl = {
    "name":"Grilled Unagi Bowl",
    "names_list":["unagi"],
    "adds_list":[],
    "base_price":1400
}

ramune = {
    "name":"Ramune",
    "names_list":["ramune"],
    "adds_list":[],
    "base_price":250
}

coca_cola = {
    "name":"Coca Cola",
    "names_list":["coke", "coca", "cola"],
    "adds_list":[],
    "base_price":100
}

sprite = {
    "name":"Sprite",
    "names_list":["sprite"],
    "adds_list":[],
    "base_price":100
}

green_tea = {
    "name":"Green Tea",
    "names_list":["tea"],
    "adds_list":[],
    "base_price":75
}

#Overall menu
menu = {
    "_id":"ozuramen@gmail.com",
    "name":"Ozu Ramen",
    "names":["ozu", "ramen"],
    "main_items":[edamame, gyoza, takoyaki, chicken_wing, salmon_share, chicken_karaage, 
    tonkotsu_ramen, tonkotsu_black_ramen, miso_ramen, spicy_miso_ramen, shoyu_ramen, shio_ramen,
    bbq_pork_bun, chicken_karaage_bun, wasabi_mini_burger, seared_salmon_plate, chicken_teriyaki, japanese_chashu_don, short_rib_lover, grilled_unagi_bowl, 
    ramune, coca_cola, sprite, green_tea],
    "link":"https://iili.io/d7Hc8u.jpg",
    "open_intro":"Welcome to Ozu Ramen!",
    "closed_intro":"Welcome to Ozu Ramen! We are currently closed but will open soon! Our hours are: [hours]",
    "delivery_time":60,
    "pickup_time":30,
    "offers_delivery":True,
    "is_open":True,
    "orders":[],
    "tax":0.06
}


cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
db = cluster["Deployment"]
collection = db["restaurants"]

collection.insert_one(menu)