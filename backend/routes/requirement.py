from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

requirement_bp = Blueprint('requirement', __name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.cpblfantasy

requirements = db.requirement

'''
Route to return a value in requirement with a given id and position
input: league(id), position(string)
return: value(int)
'''
@requirement_bp.route('/get/requirement', methods=['GET'])
def get_requirement():
    try:
        getRequirement = requirements.find_one({'_id': ObjectId(request.args.get('league'))})
        position = request.args.get('position')
        return jsonify({'value': getRequirement[position]})
    except:
        return jsonify({'value': None})
    
'''
Route to update a value in requirement with a given id
input: league(id), position(string), value(int)
return: success(boolean)
'''
@requirement_bp.route('/update/requirement', methods=['PATCH'])
def update_requirement():
    try:
        data = request.json
        if not requirements.find_one({'_id': ObjectId(data['league'])}):
            return jsonify({'success': False})    
        requirements.update_one({'_id': ObjectId(data['league'])},
                           {'$set': {data['position']: data['value']}})
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})    