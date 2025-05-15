from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables
load_dotenv()
msg = os.getenv("MESSAGE")
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

users = db.user

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return msg

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data['username']
    entry = users.find_one({"name":name})
    if entry:
        if entry['password'] == data['password']:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=True)