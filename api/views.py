import logging
import os
import json
from bson import ObjectId, json_util
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
import bcrypt
import jwt 

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')
token_key = os.getenv('TOKEN_KEY')

client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['users']
languages_collection = db['languages']
topics_collection = db['topics']
styles_collection = db['styles']

logging.basicConfig(level=logging.INFO)

# user register
@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        # Find user by email
        user = users_collection.find_one({ "email" : data['email']}) 
        if user:
            return Response({"message": "Email already exists."}, status=400)

        # Hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password': hashed_password.decode('utf-8'),
            'createdAt': datetime.datetime.now(), 
        }
        
        users_collection.insert_one(user_data)
        return Response({'message': 'User registered successfully'})
    except Exception as e:
        logging.exception("Error occurred during registration: %s", e)
        return Response({"error": "Error during the registration"}, status=500)

# user log in
@api_view(['POST'])
def login_user(request):
    try:
        data = request.data

        # check if email and password are present
        if not data.get('email') or not data.get('password'):
            return Response({"message": "Email and password are required."}, status=400)
    
        # Find user by email
        logged_user  = users_collection.find_one({ "email" : data['email']})        
        if logged_user:
             # verify the password
            if bcrypt.checkpw(data['password'].encode('utf-8'), logged_user['password'].encode('utf-8')):
                # convert ObjectId to string
                logged_user['_id'] = str(logged_user['_id'])
                del logged_user['password']  # remove password from the response

                payload = {
                    'email': logged_user['email'],
                    'id': str(logged_user['_id'])  # convert ObjectId to string
                    # add expiration
                }
                access_token = jwt.encode(payload, token_key, algorithm='HS256')

                return Response({
                    "message": "Login successful",
                    "user": logged_user,
                    "accessToken": access_token,
                }, status=200)
            else:
                return Response({"message": "Invalid credentials"}, status=401)
        else:
            return Response({
                "message": "Invalid credentials"
            }, status=401)

    except Exception as e:
        logging.exception("Error occurred during login: %s", e)
        return Response({"error": "Error logging in"}, status=500)
    


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

# helper function to parse JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))