from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

team_bp = Blueprint('team', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

leagues = db.league
teams = db.team

'''
Route to add a new league with given parameter
input: name(string), user(id), league(id)
return: success(boolean)
'''
@team_bp.route('/create/team', methods=['POST'])
def create_team():
    try:
        data = request.json
        result = teams.insert_one({
            'name': data['name'],
            'user': data['user'],
            'league': data['league'],
            'playerCount': 0
        })

        teamList = leagues.find_one({'_id': ObjectId(data['league'])})['teams']
        teamList.append(result.inserted_id)
        leagues.update_one({'_id': ObjectId(data['league'])},
                           {'$set': {'teams': teamList}})
        
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

'''
Route to return a value in team used with a given id and value
input: id(id), value_name(string)
return: request value(depends on request value)
'''
@team_bp.route('/get/team', methods=['GET'])
def get_league():
    try:
        getTeam = teams.find_one({'_id': ObjectId(request.args.get('league_name'))})
        value = request.args.get('value_name')
        return jsonify({'value': getTeam[value]})
    except:
        return jsonify({'value': None})
    
'''
Route to update a value in team used with a given id
input: id(id), value_name(string), updated_value(depends)
return: success(boolean)
'''
@team_bp.route('/update/team', methods=['PATCH'])
def update_league():
    try:
        data = request.json
        if not teams.find_one({'_id': ObjectId(data['id'])}):
            return jsonify({'success': False})    
        teams.update_one({'_id': ObjectId(data['id'])},
                           {'$set': {data['value_name']: data['updated_value']}})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    
    
'''
Route to delete a league with a given id
input: name(id)
return: success(boolean)
'''
@team_bp.route('/delete/team', methods=['DELETE'])
def delete_league():
    try:
        if not leagues.find_one({'_id': ObjectId(request.args.get('league_name'))}):
            return jsonify({'success': False})
        leagues.delete_one({'_id': ObjectId(request.args.get('league_name'))})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    