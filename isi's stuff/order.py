"""
This file contains the data structure of an customer's order.
"""


class Order:

    def __init__(self, item_list, method_of_getting_food, phone_number, order_id, address, comments):

        self.item_list = item_list
        self.method_of_getting_food = method_of_getting_food
        self.phone_number = phone_number
        self.order_id = order_id
        self.address = address
        self.comments = comments
        

