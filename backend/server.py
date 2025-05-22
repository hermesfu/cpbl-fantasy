from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import subprocess
import pandas as pd

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

users = db.user
batters = db.batter
pitchers = db.pitcher

app = Flask(__name__)
CORS(app)

'''Basic route to check the server is working'''
@app.route('/')
def home():
    return "hello world"

'''
Route to check login information and return success or not
input data: username(string), passwrod(string)
return: success(boolean)
'''
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

'''
Route to check register information and register in database if possible,
return False if the username is already been taken
input data: username(string), passwrod(string)
return: success(boolean)
'''
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['username']
    entry = users.find_one({"name":name})
    if entry:
        return jsonify({"success": False})
    else:
        user_info = {
            "name": name,
            "password": data["password"]
        }
        users.insert_one(user_info)
        return jsonify({"success": True})
    
'''
Route to return json of batter data from database
input data: batter(boolean, false if it's pitcher), categories(list of string),
            name(string), positions(list of string),
            sortby(string), ascending(boolean)
return: list of json of batter info filtered and sorted by the input request
'''
@app.route('/get_players', methods=['POST'])
def get_players():
    request_data = request.json

    if (request_data['batter']):
        player_data = batters.find({"positions":{"$in": request_data['positions']},
                                    "name":{"$regex": request_data['name']}})
    else:
        player_data = pitchers.find({"positions":{"$in": request_data['positions']},
                                    "name":{"$regex": request_data['name']}})
    player_data = pd.DataFrame(list(player_data))

    columns = ["name", "positions"]
    columns += request_data['categories']
    player_data = player_data[columns]

    player_data = player_data.sort_values(request_data['sortby'], ascending = request_data['ascending'])

    return jsonify({"data": player_data.to_json(orient="records")})

if __name__ == '__main__':
    app.run(debug=True)