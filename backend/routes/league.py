from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient

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
input: name(string), categories_p(list of string), categories_b(list of string),
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
input: league_name(string), value_name(string)
return: request value(depends on request value)
'''
@league_bp.route('/get/league', methods=['GET'])
def get_league():
    try:
        getLeague = leagues.find_one({'name': request.args.get('league_name')})
        value = request.args.get('value_name')
        return jsonify({'value': getLeague[value]})
    except:
        return jsonify({'value': None})
    
'''
Route to update a value in league used with a given league
input: league_name(string), value_name(string), updated_value(depends)
return: success(boolean)
'''
@league_bp.route('/update/league', methods=['PATCH'])
def update_league():
    try:
        data = request.json
        if not leagues.find_one({'name': data['league_name']}):
            return jsonify({'success': False})    
        leagues.update_one({'name': data['league_name']},
                           {'$set': {data['value_name']: data['updated_value']}})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    
    
'''
Route to delete a league with a given name
input: name(string)
return: success(boolean)
'''
@league_bp.route('/delete/league', methods=['DELETE'])
def delete_league():
    try:
        if not leagues.find_one({'name': request.args.get('name')}):
            return jsonify({'success': False})
        leagues.delete_one({'name': request.args.get('name')})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    