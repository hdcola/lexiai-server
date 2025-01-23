import logging
import os
import json
from bson import ObjectId
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
import bcrypt
import jwt
from django.conf import settings
from ..authentication import generate_jwt
from ..views import parse_json

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
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
        user = users_collection.find_one({"email": data['email']})
        if user:
            return Response({"message": "Email already exists."}, status=400)

        # Hash the password
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())

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
        logged_user = users_collection.find_one({"email": data['email']})
        if logged_user:
            # verify the password
            if bcrypt.checkpw(data['password'].encode('utf-8'), logged_user['password'].encode('utf-8')):
                # convert ObjectId to string
                logged_user['_id'] = str(logged_user['_id'])
                # remove password from the response
                del logged_user['password']
                logged_user['_id'] = str(logged_user['_id'])

                access_token = generate_jwt(logged_user)

                return Response({
                    "message": "Login successful",
                    "accessToken": access_token,
                    "user": logged_user,
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

# update username and email
@api_view(['PATCH'])
def update_user_profile(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response({"error": "Authorization header missing or invalid."}, status=400)

    token = auth_header.split(" ")[1]
      
    try:
        decoded_token = jwt.decode(
            token, settings.TOKEN_KEY, algorithms=['HS256'])
        logging.info(f"Decoded JWT: {decoded_token}")

        user_id = decoded_token.get('user_id')
        if not user_id:
            return Response({"error": "Invalid token: User ID missing."}, status=400)
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return Response({"error": f"User with id {user_id} not found."}, status=404)
        data = request.data
        update_result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"username": data.get('username'), "email": data.get('email')}}
        )
        if update_result.modified_count == 0:
            return Response({"message": "No changes were made."}, status=200)
        
        # the updated user
        updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
        del updated_user['password']  # remove password from the response
        updated_user['_id'] = str(updated_user['_id'])

        return Response(parse_json(updated_user), status=200)
    except Exception as e:
        logging.exception("Error occurred during updating user profile: %s", e)
        return Response({"error": "Error updating user profile"}, status=500)

