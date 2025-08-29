from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import math
from bson.objectid import ObjectId
import json
import numpy as np

player_bp = Blueprint('player', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

batters = db.batter
pitchers = db.pitcher
player_state = db.player_state

'''
Route to return json of player data from database
input: iaBatter(boolean, false if it's pitcher), categories(list of string),
            name(string), positions(list of string), team(string)
            sortby(string), ascending(boolean),
            page(int), league(id)
return: data(list of json of players info filtered and sorted by the input request, 25 rows each page)
        totalPage(int of total page of data)
        curPage(int of current page)
'''
@player_bp.route('/get/players', methods=['POST'])
def get_players():
    try:
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

        all_categories = ['_id'] + request_data['categories']
        player_data = player_data[all_categories]
        player_data = player_data.sort_values(request_data['sortby'], ascending = request_data['ascending'])

        totalPage = math.ceil(player_data.shape[0] / 25)
        start = (request_data['page'] - 1) * 25
        end = start + 25

        if start > player_data.shape[0]:
            player_data = player_data[start :]
        else:
            player_data = player_data[start : end]

        player_data['_id'] = player_data['_id'].apply(str)
        player_data['status'] = player_data['_id'].apply(lambda id: 
                                                         player_state.find_one({"league": ObjectId(request_data['league']),
                                                        "player": ObjectId(id)}))
        player_data['status'] = player_data['status'].apply(lambda entry: 
                                                         str(entry['team']) if entry else None)
                        
        return jsonify({"data": player_data.to_dict(orient="records"), "totalPage": totalPage})
    except:
        return jsonify({"data": None, "totalPage": 0})
    
'''
Route to return json of player data from database with given players id
input: players(2D list of [position, id]), categories(list of string), isBatter(boolean)
return: data(list of json of players info)
'''
@player_bp.route('/search/players', methods=['POST'])
def search_players():
    try:
        data = request.json
        all_data = pd.DataFrame()

        for player in data['players']:
            if player[1]:
                player_data = None
                if data['isBatter']:
                    player_data = batters.find_one({"_id": ObjectId(player[1])})
                else:
                    player_data = pitchers.find_one({"_id": ObjectId(player[1])})

                player_data = pd.DataFrame([player_data])       

                player_data = player_data[data['categories']]
                player_data["_id"] = player[1]
                player_data["position"] = player[0]
            else:
                #fill up with None
                player_data = {}
                for c in data['categories']:
                    player_data[c] = None
                player_data["_id"] = player[1]
                player_data["position"] = player[0]
                player_data = pd.DataFrame(player_data, index=[0])

            all_data = pd.concat([all_data, player_data],  ignore_index = True)

        json_string_data = all_data.to_json(orient="records")
        python_data_structure = json.loads(json_string_data)
        return jsonify({"data": python_data_structure})
    except Exception as e:
        print(e)
        return jsonify({"data": None})