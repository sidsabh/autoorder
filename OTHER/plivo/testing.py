#from flask import Flask, request, session
#from sample_menu import *
#from methods import *
import pymongo
from pymongo import MongoClient
#from primary_methods import *

#import g
import stripe
'''
stripe.api_key = 'sk_test_51H7n9PDTJ2YcvBWss1pfBvdXC70jEZ8wV4vpVhF0dViTlNRc9kRigRMJfJSoi6lYCJclszW3Ejx9qDXcCWwvtWyF00KHSY6yyV'

session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[{
            
            'price_data': {
                'unit_amount': 400000,
                'currency': 'usd',
                'product': 'prod_HifPkxqBklYeQl',
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='https://www.google.com',
        cancel_url='https://www.google.com',
    )

print(session.id)
'''

cluster = MongoClient("mongodb+srv://admin:54230283752976456@maincluster.ntyoc.mongodb.net/Index?retryWrites=true&w=majority")
db = cluster["Index"]
col = db["our_numbers"]
col.insert_one({"_id":"+14133317017", "codes":["0001","0002"], "index_message":"Welcome to the random restaurant index!"})

