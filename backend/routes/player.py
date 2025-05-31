from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import math

player_bp = Blueprint('player', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

batters = db.batter
pitchers = db.pitcher

'''
Route to return json of batter data from database
input: iaBatter(boolean, false if it's pitcher), categories(list of string),
            name(string), positions(list of string), team(string)
            sortby(string), ascending(boolean),
            page(int)
return: data(list of json of batter info filtered and sorted by the input request, 25 rows each page)
        totalPage(int of total page of data)
        curPage(int of current page)
'''
@player_bp.route('/get/players', methods=['POST'])
def get_players():
    request_data = request.json

    if (request_data['iaBatter']):
        player_data = batters.find({"positions":{"$in": request_data['positions']},
                                    "name":{"$regex": request_data['name']},
                                    "team":{"$regex": request_data['team']}})
    else:
        player_data = pitchers.find({"positions":{"$in": request_data['positions']},
                                    "name":{"$regex": request_data['name']},
                                    "team":{"$regex": request_data['team']}})
    player_data = pd.DataFrame(list(player_data))

    player_data = player_data[request_data['categories']]
    player_data = player_data.sort_values(request_data['sortby'], ascending = request_data['ascending'])

    totalPage = math.ceil(player_data.shape[0] / 25)
    start = (request_data['page'] - 1) * 25 + 1
    end = start + 25

    if start > player_data.shape[0]:
        player_data = player_data[start :]
    else:
        player_data = player_data[start : end]
    
    return jsonify({"data": player_data.to_dict(orient="records"), "totalPage": totalPage})