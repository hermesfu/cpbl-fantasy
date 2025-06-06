from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

roster_bp = Blueprint('roster', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

rosters = db.roster
teams = db.team
player_state = db.player_state

'''
Route to return a player list in roster with a given id and position
input: team(id), position(string)
return: players(list of id)
'''
@roster_bp.route('/get/roster', methods=['GET'])
def get_roster():
    try:
        getRoster = rosters.find_one({'_id': ObjectId(request.args.get('team'))})
        position = request.args.get('position')
        return jsonify({'players': getRoster[position]})
    except:
        return jsonify({'players': None})

'''
Route to add a player to a team roster
input: team(id), position(string), player(id)
return: success(boolean)
'''
@roster_bp.route('/add/player', methods=['POST'])
def add_player():
    try:
        data = request.json
        updated_team = teams.find_one({"_id": ObjectId(data['team'])})

        if not updated_team:
            return jsonify({'success': False})
        
        rosters.update_one({"_id": ObjectId(data['team'])},
                        {"$push": {data['position']: data['player']}})
        teams.update_one({"_id": ObjectId(data['team'])},
                         {"$inc": {"playerCount": 1}})
        
        player_state.insert_one({'player': data['player'],
                              'league': updated_team['league'],
                              'team': data['team']})
        
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

'''
Route to drop a player from a team roster
input: team(id), position(string), player(id)
return: success(boolean)
'''
@roster_bp.route('/drop/player', methods=['POST'])
def drop_player():
    try:
        data = request.json
        if not teams.find_one({"_id": ObjectId(data['team'])}):
            return jsonify({'success': False})
        
        rosters.update_one({"_id": ObjectId(data['team'])},
                        {"$pull": {data['position']: data['player']}})
        teams.update_one({"_id": ObjectId(data['team'])},
                         {"$inc": {"playerCount": -1}})
        
        player_state.delete_one({"team": data['team'],
                                 "player": data['player']})
        
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

'''
Route to swap two players in a team roster
input: team(id), position1(string), player1(id), position2(string), player2(id)
return: success(boolean)
'''
@roster_bp.route('/swap/player', methods=['POST'])
def swap_player():
    try:
        data = request.json
        if not rosters.find_one({"_id": data['team']}):
            return jsonify({'success': False})
        
        rosters.update_one({"_id": data['team']},
                        {"$push": {data['position1']: data['player2']}},
                        {"$push": {data['position1']: data['player1']}})
        rosters.update_one({"_id": data['team']},
                        {"$push": {data['position2']: data['player1']}},
                        {"$push": {data['position2']: data['player2']}})
        
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})