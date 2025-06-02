from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

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
input: name(string, required), categories_p(list of string), categories_b(list of string),
       positions(json), isPointLeague(boolean),
       teams(list of id), maxTeams(int)
return: success(boolean)
'''
@league_bp.route('/create/league', methods=['POST'])
def create_league():
    try:
        data = request.json
        if (leagues.find_one({'name': data['name']})):
            return jsonify({"success": False})

        teamSetting = {
            'name': data['name'],
            'categories_p': data.get('categories_p', ['W', 'SO', 'SV', 'ERA', 'WHIP']),
            'categories_b': data.get('categories_c', ['avg', 'R', 'RBI', 'HR', 'SB']),
            'isPointLeague': data.get('isPointLeague', False),
            'teams': [],
            'maxTeams': data.get('maxTeams', 12)
        }

        leagues.insert_one(teamSetting)
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

'''
Route to return a value in league used with a given league and value
input: league(id), value(string)
return: request value(depends on request value)
'''
@league_bp.route('/get/league', methods=['GET'])
def get_league():
    try:
        getLeague = leagues.find_one({'_id': ObjectId(request.args.get('league'))})
        value = request.args.get('value')
        return jsonify({'value': getLeague[value]})
    except:
        return jsonify({'value': None})
    
'''
Route to update a value in league used with a given league id
input: league(id), value_name(string), updated_value(depends)
return: success(boolean)
'''
@league_bp.route('/update/league', methods=['PATCH'])
def update_league():
    try:
        data = request.json
        if not leagues.find_one({'_id': ObjectId(data['league'])}):
            return jsonify({'success': False})    
        leagues.update_one({'_id': ObjectId(data['league'])},
                           {'$set': {data['value_name']: data['updated_value']}})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    
    
'''
Route to delete a league with a given league id
input: league(id)
return: success(boolean)
'''
@league_bp.route('/delete/league', methods=['DELETE'])
def delete_league():
    try:
        if not leagues.find_one({'_id': ObjectId(request.args.get('league'))}):
            return jsonify({'success': False})
        leagues.delete_one({'_id': ObjectId(request.args.get('league'))})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    