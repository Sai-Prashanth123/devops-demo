import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL not set")
else:
    print("MONGO_URL found")

client = MongoClient(MONGO_URL)
db = client["fastapi"]
user_collection = db["sample_data"]
print("Database and collection initialized")