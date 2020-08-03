"""
This file stores our methods for sending messages.
"""

from settings import *
from essentials import *

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

#sends a singular message and exits the app
def send_message(resp):
    response = MessagingResponse()
    response.message(resp)
    return str(response)

#sends a singular message and the menu and exits the app
def send_message_and_menu(msg, resp):
    client.messages.create(
    to=msg.fro,
    from_=msg.to,
    body=None,
    media_url=msg.rinfo["link"]
    )
    response = MessagingResponse()
    response.message(resp)
    return str(response)

#sends a singular message without exiting the app
def send_message_client(message, to_no, from_no):
    client.messages.create(
    to=to_no,
    from_=from_no,
    body=message
    )