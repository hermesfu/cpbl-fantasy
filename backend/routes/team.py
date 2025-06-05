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
users = db.user
rosters = db.roster

'''
Route to add a new team with given parameter
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

        rosters.insert_one({
            '_id': result.inserted_id,
            'C': [],
            '1B': [],
            '2B': [],
            '3B': [],
            'SS': [],
            'LF': [],
            'CF': [],
            'RF': [],
            'IF': [],
            'OF': [],
            'Util': [],
            'SP': [],
            'RP': [],
            'P': [],
            'BEN': [],
            'O': []
        })

        leagues.update_one({'_id': ObjectId(data['league'])},
                           {"$push": {"teams": str(result.inserted_id)}})
        users.update_one({'_id': ObjectId(data['user'])},
                           {"$push": {"teams": str(result.inserted_id)}})
        
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

'''
Route to return a value in team used with a given id and value
input: team(id), value(string)
return: request value(depends on request value)
'''
@team_bp.route('/get/team', methods=['GET'])
def get_team():
    try:
        getTeam = teams.find_one({'_id': ObjectId(request.args.get('team'))})
        value = request.args.get('value')
        return jsonify({'value': getTeam[value]})
    except:
        return jsonify({'value': None})
    
'''
Route to update a value in team used with a given id
input: team(id), value_name(string), updated_value(depends)
return: success(boolean)
'''
@team_bp.route('/update/team', methods=['PATCH'])
def update_team():
    try:
        data = request.json
        if not teams.find_one({'_id': ObjectId(data['team'])}):
            return jsonify({'success': False})    
        teams.update_one({'_id': ObjectId(data['team'])},
                           {'$set': {data['value_name']: data['updated_value']}})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    
    
'''
Route to delete a team with a given id
input: team(id)
return: success(boolean)
'''
@team_bp.route('/delete/team', methods=['DELETE'])
def delete_team():
    try:
        teamToDelete = teams.find_one({'_id': ObjectId(request.args.get('team'))})
        if not teamToDelete:
            return jsonify({'success': False})
        
        leagues.update_one({'_id': ObjectId(teamToDelete['league'])},
                           {"$pull": {"teams": request.args.get('team')}})
        users.update_one({'_id': ObjectId(teamToDelete['user'])},
                           {"$pull": {"teams": request.args.get('team')}})

        teams.delete_one({'_id': ObjectId(request.args.get('team'))})
        rosters.delete_one({'_id': ObjectId(request.args.get('team'))})

        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    