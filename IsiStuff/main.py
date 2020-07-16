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

    #session.clear()
    print(session)

    #get the message that was sent and make it all lowercase
    incoming_msg = request.values.get('Body', None)
    incoming_msg = incoming_msg.lower()

    #get the phone number of the incoming msg
    phone_number = request.values.get('From', None)

    #get the section of the order process the customer is in
    section = session.get('section', "first_message")
    
    #if this is the first message that the customer sends
    if section == "first_message":
        return first_message(incoming_msg, phone_number)

    #if the customer is in the ordering process
    if section == "ordering_process":
        return ordering_process(incoming_msg)

    #if the customer just indicated they are finished ordering
    if section == "finished_ordering":
        return finished_ordering(incoming_msg)



#triggered if the message sent is the first message the customer has sent in 4 hours I think because that is when the session is cleared
def first_message(incoming_msg, phone_number):
    
    #initialize order object
    #session["order"] = Order([], "pickup", phone_number, 346356457, None, None)
    #session["order"] = {"item_list":[], "method_of_getting_food":"pickup", "phone_number":phone_number, "order_id":1234, "address":None, "comments":None}

    #update the section of the process
    session["section"] = "ordering_process"
    
    #send the restaurant's custom intro message
    return send_message(menu.intro_message)



#triggered if the customer is in the middle of the ordering process
def ordering_process(incoming_msg):

    #if the customer indicates they are done ordering
    if "finish" in incoming_msg:
        session["section"] = "finished_ordering"
        return send_message("Thank you for your order. It will be processed shortly.")
    
    #get the main item the customer ordered
    main_item_or_error_code = get_main_item(incoming_msg)

    #if no specific main item was detected
    if main_item_or_error_code == 0:
        return send_message("It seems you did not order any of the main items on our menu. Please try again.")
    if main_item_or_error_code == 1:
        return send_message("It seems you have order too many main items. Please try again and only order one main item.")
    if main_item_or_error_code == 2:
        return send_message("It seems you have order too many main items. Please try again and only order one main item. ERROR CODE 2")
    
    #if a specific main item was detected
    else:
        
        session["order"]["item_list"].append(main_item_or_error_code)
        print(session)
        response = ""
        for item in session["order"]["item_list"]:
            response = response +"%s. " %item.name
        response = response+'What else would you like? If you would like to restart your order please text "restart." If that is all please text "finished."'
        return send_message(response)



def finished_ordering(incoming_msg):

    session["section"] = "first_message"
    return send_message("ur done")
    



if __name__ == "__main__":
    app.run(debug=True)

