"""
This is the main code. Our program uses the flask web framework in combination with Twilio's API for sending sms messages
to enable text message ordering for restaurants.
"""


from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from menu import *
from order import *
from sample_menu import *
from methods import *


# The session object makes use of a secret key.
SECRET_KEY = "kj43j34btw8er93brwerb2395834ghr3urhw4u3r7h2u3hr2j3br34876rv87t"
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def main():
    
    #get the message that was sent and make it all lowercase
    incoming_msg = request.values.get('Body', None)
    incoming_msg = incoming_msg.lower()

    #get the section of the order process the customer is in
    section = session.get('section', "first_message")
    
    #if this is the first message that the customer sends
    if section == "first_message":
        return first_message(incoming_msg)

    #if the customer is in the ordering process
    if section == "ordering_process":
        return ordering_process(incoming_msg)

    #if the customer just indicated they are finished ordering
    if section == "finished_ordering":
        return finished_ordering(incoming_msg)


#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message(incoming_msg):

    session["section"] = "ordering_process"
    return send_message("Thanks for contacting Mario's Pizzeria! Here is our menu, what is the first item you would like?")


def ordering_process(incoming_msg):

    if "finish" in incoming_msg:
        session["section"] = "finished_ordering"
        return send_message("Thank you for your order. It will be processed shortly.")
    
    main_item = get_main_item(incoming_msg)
    return send_message("%s detected. What else?") % main_item.name


def finished_ordering(incoming_msg):

    session["section"] = "first_message"
    return send_message("ur done")
    



if __name__ == "__main__":
    app.run(debug=True)

