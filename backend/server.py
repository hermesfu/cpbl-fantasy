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
input: username(string), passwrod(string)
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
input: username(string), passwrod(string)
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
Route to return the categories used with a given league
input: league_name(string)
return: categories(list of string)
'''
@app.route('/get/categories', methods=['GET'])
def get_categories():
    position = request.args.get('position')
    if 'P' in position:
        return jsonify({"categories": ["name", "team", "positions", "W", "L", "SV", "SO", "ERA"]})
    return jsonify({"categories": ["name", "team", "positions", "H", "HR", "R", "RBI", "SB"]})
    
'''
Route to return json of batter data from database
input: iaBatter(boolean, false if it's pitcher), categories(list of string),
            name(string), positions(list of string), team(string)
            sortby(string), ascending(boolean)
return: list of json of batter info filtered and sorted by the input request
'''
@app.route('/get/players', methods=['POST'])
def get_players():
    request_data = request.json

    if (request_data['iaBatter']):
        player_data = batters.find({"positions":{"$in": request_data['positions']},
                                    "name":{"$regex": request_data['name']},
                                    "team":{"$regex": request_data['team']}})
    else:
        player_data = pitchers.find({"positions":{"$in": request_data['positions']},
                                    "name":{"$regex": request_data['name']}})
    player_data = pd.DataFrame(list(player_data))

    player_data = player_data[request_data['categories']]
    player_data = player_data.sort_values(request_data['sortby'], ascending = request_data['ascending'])

    return jsonify({"data": player_data.to_dict(orient="records")})

if __name__ == '__main__':
    app.run(debug=True)