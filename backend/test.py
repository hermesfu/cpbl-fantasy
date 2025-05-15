from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
msg = os.getenv("MESSAGE")
mongo_url = os.getenv("MONGO_URI")

client = MongoClient(mongo_url)

db = client.cpblfantasy
users = db.user

found = users.find_one({"name":"d"})
if (found):
    print(found['password'])
else:
    print("not found")