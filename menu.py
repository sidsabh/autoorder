"""
This file contains the data structure that restaurants will need to input in order to use our program.
"""


#overall menu
class Menu:

    def __init__(self, restaurant_name, mains_list, intro_message, closed_message, offers_delivery, delivery_time, pickup_time, is_open):
        self.restaurant_name = restaurant_name
        self.mains_list = mains_list
        self.intro_message = intro_message
        self.closed_message = closed_message
        self.offers_delivery = offers_delivery
        self.delivery_time = delivery_time
        self.pickup_time = pickup_time
        self.is_open = is_open

menu = {
    "restaurant_name":str,
    "open_intro_message":str,
    "closed_intro_message":str,
    "delivery_time":int,
    "pickup_time":int,
    "offers_delivery":bool,
    "is_open":bool
    "main_items":list,
}
    

#primary items on the menu
class MainItem:

    def __init__(self, name, names_list, adds_list, base_price):
        self.name = name
        self.names_list = names_list
        self.adds_list = adds_list
        self.base_price = base_price

main_item = {
    "name":str,
    "names_list":list,
    "adds_list":list,
    "base_price":float
}


#a specific list of add-ons for a main item
class AddOnList:

    def __init__(self, name, choice_list, min_choices, max_choices, prompting_question):
        self.name = name
        self.choice_list = choice_list
        self.min_choices = min_choices
        self.max_choices = max_choices
        self.prompting_question = prompting_question

add_on_list = {
    "name":str,
    "choice_list":list,
    "min_choices":int,
    "max_choices":int,
    "prompting_question":str
    "sublist_inceptions":list
}


#an item in the add-on list
class AddOnChoice:

    def __init__(self, name, names_list, add_price):
        self.name = name
        self.names_list = names_list
        self.add_price = add_price
        #has quantity

add_on_choice = {
    "name":str,
    "names_list":str,
    "add_price":float
}

