from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd

matchup_bp = Blueprint('matchup', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

matchups = db.matchup

'''
Route to add a new matchup with given parameter
input: legue(id), team1(id), team2(id), start(date), end(date)
return: success(boolean)
'''
@matchup_bp.route('/create/matchup', methods=['POST'])
def create_matchup():
    try:
        data = request.json
        matchups.insert_one({'league': data['league'], 'team1': data['team1'], 'team2': data['team2'],
                          'start': data['start'], 'end': data['end']})

        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

'''
Route to return values in matchup with a given league and value
input: matchup(id), values(string)
return: request values(json)
'''
@matchup_bp.route('/get/matchup', methods=['GET'])
def get_matchup():
    try:
        getMatchup = matchups.find_one({'_id': ObjectId(request.args.get('matchup'))})
        value = request.args.get('value')
        return jsonify({'value': getMatchup[value]})
    except:
        return jsonify({'value': None})
    
'''
Route to update a value in matchup used with a given matchup id
input: matchup(id), value_name(string), updated_value(depends)
return: success(boolean)
'''
@matchup_bp.route('/update/matchup', methods=['PATCH'])
def update_matchup():
    try:
        data = request.json
        if not matchups.find_one({'_id': ObjectId(data['matchup'])}):
            return jsonify({'success': False})    
        matchups.update_one({'_id': ObjectId(data['matchup'])},
                           {'$set': {data['value_name']: data['updated_value']}})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False}) 
    
'''
Route to calculate the total of each column from a table of player data
sum up for integer, mean for float
input: data(table)
output: dictionary
'''
@matchup_bp.route('/calculate/total', methods=['POST'])
def calculate_total():
    try:
        df = pd.DataFrame(request.json['data'])
        result = {}
        for c in df.columns:
            if df[c].dtype == "int64" or df[c].dtype == "int32":
                result[c] = int(df[c].sum())
            elif df[c].dtype == "float64" or df[c].dtype == "float32":
                result[c] = float(df[c].mean())
        return jsonify(result)
    except:
        return jsonify({'sucess': False})