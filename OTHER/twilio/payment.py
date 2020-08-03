"""
This file works with Stripe, our payment api.
"""

from settings import *
from essentials import *

from messaging import *

import stripe



"""
Sends the user a link to checkout.
"""
def checkout(msg):
    
    stripe.api_key = STRIPE_API_KEY
    product_id = STRIPE_PRODUCT_ID

    #if this is the demo number then use development credentials even if in deployment
    if msg.to == "+12676276054":
        product_id = STRIPE_TEST_PRODUCT_ID
        stripe.api_key = STRIPE_TEST_API_KEY

    #creates a checkout session with stripe api
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[{
            
            'price_data': {
                'unit_amount': int((subtotal(msg)+tax(msg))*100),
                'currency': 'usd',
                'product': product_id,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='https://dashboard.autoordersystems.com/success/',
        cancel_url='https://dashboard.autoordersystems.com/failure/',
    )

    #stores the unique id
    OPC.update_one(current_order(msg), {"$set":{"payment_intent":session.payment_intent}})

    #craft response
    resp = "Here is your link to checkout. Your order will be processed once you pay. \n\nhttps://dashboard.autoordersystems.com/checkout/{id}".format(id=session.id)
    if msg.to == "+12676276054":
        resp += "\n\nDEMO: Use 4242 4242 4242 4242 as the credit card number. Type in anything for the rest of the information."

    return send_message(resp)