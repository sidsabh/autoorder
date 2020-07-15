"""
This file contains supplementary methods that may be used in the main file.
"""


from twilio.twiml.messaging_response import MessagingResponse
from menu import *
from sample_menu import *


"""
Sends a message.
Input: Message to be sent (string)
Returns: a message (string)
"""
def send_message(msg):
    resp = MessagingResponse()
    resp.message(msg)
    return str(resp)


"""
Finds the main item the customer wants.
Input: Message (string)
Returns: Main Item indicated (MainItem)
"""
def get_main_item(incoming_msg):

    possible_main_items = []

    for main_item in menu.mains_list:
        
        for name in main_item.names_list:
            
            if name in incoming_msg:

                possible_main_items.append(main_item)
    
    return possible_main_items[0]

    
                



