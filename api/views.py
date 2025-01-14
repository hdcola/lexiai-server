import logging
import os
import json
from bson import ObjectId, json_util
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')

client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['users']
languages_collection = db['languages']
topics_collection = db['topics']
styles_collection = db['styles']

logging.basicConfig(level=logging.INFO)

# users
@api_view(['POST'])
def register_user(request):
    data = request.data

    user_data = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],
        'createdAt': datetime.datetime.now(), 
    }
    
    users_collection.insert_one(user_data)
    return Response({'message': 'User registered successfully'})

# Languages
@api_view(['GET'])
def get_all_languages(request):
    languages = languages_collection.find({})
    return Response(parse_json(languages))


# get all AI styles
@api_view(['GET'])
def get_all_ai_styles(request):
    try:
        styles = styles_collection.find({})
        logging.info(styles)
        return Response(parse_json(styles))
    except Exception as e:
        logging.exception(e) # automatically takes care of getting the traceback for the current exception and logging
        return Response({"error": "Failed to fetch styles"}, status=500)


# get topics for language and level
@api_view(['GET'])
def get_topics_for_level(request):
    level = request.GET.get('level')
    try:
        topics = topics_collection.find({ "level": level })
        topics_list = list(topics)
        if not topics_list:
            return Response({"message": "No topics found for the specified level."}, status=404)

        return Response(parse_json(topics_list))
    except Exception as e:
        logging.exception("Error fetching topics for language and level: %s", e)
        return Response({"message": "An error occurred while fetching topics."}, status=500)


def parse_json(data):
    return json.loads(json_util.dumps(data))