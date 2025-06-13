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
requirements = db.requirement
batters = db.batter
pitchers = db.pitcher

'''
Route to return a player list in roster with a given team id and position
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
Route to return a 2D list of an entire team roster with a given team id
input: team(id), isBatter(boolean)
return: players(2D list [string, id])
'''    
@roster_bp.route('/get/rosters', methods=['GET'])
def get_rosters():
    positions = []
    if request.args.get('isBatter') == "true":
        positions = ["C", "1B", "2B", "3B", "SS", "IF", "LF", "CF", "RF", "OF", "Util"]
    else:
        positions = ["SP", "RP", "P"]
    players = []

    try:
        roster = rosters.find_one({"_id": ObjectId(request.args.get('team'))})
        requirement = requirements.find_one({"_id": ObjectId(teams.find_one({"_id": ObjectId(request.args.get('team'))})['league'])})

        for position in positions:
            for p in roster[position]:
                players.append([position, p])
            for i in range(requirement[position] - len(roster[position])):
                players.append([position, None])

        #bench and out can be either batter or pitcher, so making sure here
        for p in roster['BEN']:
            if ((request.args.get('isBatter') == "true") and batters.find_one({"_id": ObjectId(p)})) or ((request.args.get('isBatter') == "false") and pitchers.find_one({"_id": ObjectId(p)})):
               players.append(['BEN', p])
        for p in roster['O']:
            if ((request.args.get('isBatter') == "ture") and batters.find_one({"_id": ObjectId(p)})) or ((request.args.get('isBatter') == "false") and pitchers.find_one({"_id": ObjectId(p)})):
               players.append(['O', p])

        return jsonify({'players': players})  
    except:
        return jsonify({'players': None})

'''
Route to add a player to a team roster
input: team(id), player(id), positions(list of string)
return: success(boolean)
'''
@roster_bp.route('/add/player', methods=['POST'])
def add_player():
    try:
        data = request.json
        updated_team = teams.find_one({"_id": ObjectId(data['team'])})

        if not updated_team:
            return jsonify({'success': False})
        
        requirment = requirements.find_one({"_id": ObjectId(updated_team['league'])})
        roster = rosters.find_one({"_id": ObjectId(data['team'])})
        addPosition = None
        for position in (data['positions'] + ["BEN"]):
            if requirment[position] > len(roster[position]):
                addPosition = position
                break

        if not addPosition:
            return jsonify({'success': False})
        
        rosters.update_one({"_id": ObjectId(data['team'])},
                        {"$push": {addPosition: data['player']}})
        teams.update_one({"_id": ObjectId(data['team'])},
                         {"$inc": {"playerCount": 1}})
        
        player_state.insert_one({'player': ObjectId(data['player']),
                              'league': ObjectId(updated_team['league']),
                              'team': ObjectId(data['team'])})
        
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
        
        player_state.delete_one({"team": ObjectId(data['team']),
                                 "player": ObjectId(data['player'])})
        
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

'''
Route to swap two players in a team roster
input: team(id), player1(id), position1(string),
                 player2(id), position2(string), positions2(list of string),
return: success(boolean)
'''
@roster_bp.route('/swap/player', methods=['POST'])
def swap_player():
    try:
        data = request.json
        if not rosters.find_one({"_id": ObjectId(data['team'])}):
            return jsonify({'success': False})
        
        rosters.update_one({"_id": ObjectId(data['team'])},
                           {
                                "$push": {data['position2']: data['player1']},
                                "$pull": {data['position1']: data['player1']},
                                "$push": {data['position1']: data['player2']},
                                "$pull": {data['position2']: data['player2']}
                           })
        
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False})