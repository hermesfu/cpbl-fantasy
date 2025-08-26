from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient

user_bp = Blueprint('user', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

users = db.user

'''
Route to check login information and return success or not
input: username(string), passwrod(string)
return: success(boolean)
'''
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data['username']
    entry = users.find_one({"name":name})
    if entry:
        if entry['password'] == hash(data['password']):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})

'''
Route to check register information and register in database if possible,
return False if the username is already been taken
input: username(string), passwrod(string)
return: success(boolean)
'''
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['username']
    entry = users.find_one({"name":name})
    if entry:
        return jsonify({"success": False})
    else:
        user_info = {
            "name": name,
            "password": hash(data["password"]),
            "teams": []
        }
        users.insert_one(user_info)
        return jsonify({"success": True})