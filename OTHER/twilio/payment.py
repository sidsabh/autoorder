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
    if msg.to == "+12676276054":
        stripe.api_key = "sk_test_51H7n9PDTJ2YcvBWss1pfBvdXC70jEZ8wV4vpVhF0dViTlNRc9kRigRMJfJSoi6lYCJclszW3Ejx9qDXcCWwvtWyF00KHSY6yyV"

    #creates a checkout session with stripe api
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[{
            
            'price_data': {
                'unit_amount': int(total_cost(msg)*100),
                'currency': 'usd',
                'product': 'prod_HifPkxqBklYeQl',
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='http://dashboard.autoordersystems.com/success/',
        cancel_url='http://dashboard.autoordersystems.com/failure/',
    )

    #stores the unique id
    OPC.update_one(current_order(msg), {"$set":{"payment_intent":session.payment_intent}})

    #craft response
    resp = "Here is your link to checkout. Your order will be processed once you pay. \n\nhttp://dashboard.autoordersystems.com/checkout/{id}".format(id=session.id)
    if msg.to == "+12676276054":
        resp += "\n\nDEMO: Use 4242 4242 4242 4242 as the credit card number. Type in anything for the rest of the information."

    return send_message(resp)