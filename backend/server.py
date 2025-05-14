from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables
load_dotenv()
msg = os.getenv("MESSAGE")
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = client = MongoClient(mongo_url)

app = Flask(__name__)

@app.route('/')
def home():
    return msg

if __name__ == '__main__':
    app.run(debug=True)