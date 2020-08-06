"""
This file sets up our environment variables.
"""


# settings.py
from dotenv import load_dotenv
import os

import pymongo
from pymongo import MongoClient

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



ENVIRONMENT = os.getenv("ENVIRONMENT")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

SENTRY_DSN = os.getenv("SENTRY_DSN")

STRIPE_TEST_SECRET_ENDPOINT = os.getenv("STRIPE_TEST_SECRET_ENDPOINT")
STRIPE_LIVE_SECRET_ENDPOINT = os.getenv("STRIPE_LIVE_SECRET_ENDPOINT")

STRIPE_TEST_PRODUCT_ID = os.getenv("STRIPE_TEST_PRODUCT_ID")

STRIPE_TEST_API_KEY = os.getenv("STRIPE_TEST_API_KEY")

CLUSTER_ID = os.getenv("CLUSTER_ID")
CLUSTER = MongoClient(CLUSTER_ID)

if ENVIRONMENT == "development":
    DB = CLUSTER["Development"]
    STRIPE_API_KEY = os.getenv("STRIPE_TEST_API_KEY")
    STRIPE_PRODUCT_ID = os.getenv("STRIPE_TEST_PRODUCT_ID")

if ENVIRONMENT == "deployment":
    DB = CLUSTER["Deployment"]
    STRIPE_API_KEY = os.getenv("STRIPE_LIVE_API_KEY")
    STRIPE_PRODUCT_ID = os.getenv("STRIPE_LIVE_PRODUCT_ID")


ONC = DB["our_numbers"]
UNC = DB["user_numbers"]
OPC = DB["order_process"]
RC = DB["restaurants"]
OC = DB["orders"]