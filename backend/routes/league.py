from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import math

league_bp = Blueprint('league', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

leagues = db.league

'''
Route to add a new league with given parameter
input: name(string), categories_p(list of string), categories_c(list of string),
       positions(json), isPointLeague(boolean),
       teams(list of id), maxTeams(int)
return: success(boolean)
'''
@league_bp.route('/create/league', methods=['POST'])
def create_league():
    data = request.json
    if (leagues.find_one({'name': data['name']})):
        return jsonify({"success": False})
    
    default_positions = jsonify({'C': 1, '1B': 1, '2B': 1, '3B': 1, 'SS': 1,
                                 'OF': 3, 'Util': 3,
                                 'SP': 2, 'RP': 2, 'P': 4,
                                 'BEN': 4, 'O': 2})

    teamSetting = {
        'name': data['name'],
        'categories_p': data.get('categories_p', ['W', 'SO', 'SV', 'ERA', 'WHIP']),
        'categories_c': data.get('categories_c', ['AVG', 'R', 'RBI', 'HR', 'SB']),
        'isPointLeague': data.get('isPointLeague', False),
        'teams': [],
        'maxTeams': data.get('maxTeams', 12)
    }

    leagues.insert_one(teamSetting)
    return jsonify({"success": True})

'''
Route to return a value in league used with a given league and value
input: league_name(string), value_name(string)
return: request value(depends on request value)
'''
@league_bp.route('/get/league', methods=['GET'])
def get_league():
    getLeague = leagues.find_one({'name': request.args.get('league_name')})
    value = request.args.get('value_name')
    if (not getLeague):
        return jsonify({value: None})

    return jsonify({value: getLeague[value]})