import logging
import json
from bson import ObjectId, json_util
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import bcrypt
import jwt
from django.conf import settings
from .authentication import generate_jwt

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db['users']
languages_collection = db['languages']
topics_collection = db['topics']
styles_collection = db['styles']

logging.basicConfig(level=logging.INFO)

# Languages


@api_view(['GET'])
def get_all_languages(request):
    languages = languages_collection.find({})
    return Response(parse_json(languages))

# Language by id


@api_view(['GET'])
def get_language_by_id(request, id: str):
    try:
        language = languages_collection.find_one({"_id": ObjectId(id)})
        if not language:
            return Response({"error": f"Language with id {id} not found."}, status=404)

        return Response(parse_json(language), status=200)
    except Exception as e:
        logging.exception("Error fetching language by id: %s", e)
        return Response({"error": "Failed to fetch language with id: ${id}"}, status=500)


# get all AI styles
@api_view(['GET'])
def get_all_ai_styles(request):
    try:
        styles = styles_collection.find({})
        logging.info(styles)
        return Response(parse_json(styles))
    except Exception as e:
        # automatically takes care of getting the traceback for the current exception and logging
        logging.exception(e)
        return Response({"error": "Failed to fetch styles"}, status=500)


# style by id
@api_view(['GET'])
def get_ai_style_by_id(request, id: str):
    try:
        style = styles_collection.find_one({"_id": ObjectId(id)})
        if not style:
            return Response({"error": f"style with id {id} not found."}, status=404)

        return Response(parse_json(style), status=200)
    except Exception as e:
        logging.exception("Error fetching style by id: %s", e)
        return Response({"error": "Failed to fetch style with id: ${id}"}, status=500)

# get topics for language and level


@api_view(['GET'])
def get_topics_for_level(request):
    level = request.GET.get('level')
    try:
        topics = topics_collection.find({"level": level})
        topics_list = list(topics)
        if not topics_list:
            return Response({"message": "No topics found for the specified level."}, status=404)

        return Response(parse_json(topics_list))
    except Exception as e:
        logging.exception(
            "Error fetching topics for language and level: %s", e)
        return Response({"message": "An error occurred while fetching topics."}, status=500)

# helper function to parse JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))


# validate JWT
@api_view(['GET'])
def validate_jwt(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response({"error": "Authorization header missing or invalid."}, status=status.HTTP_400_BAD_REQUEST)

    token = auth_header.split(" ")[1]

    try:
        decoded_token = jwt.decode(
            token, settings.TOKEN_KEY, algorithms=['HS256'])
        logging.info(f"Decoded JWT: {decoded_token}")

        user_id = decoded_token.get('user_id')
        if not user_id:
            return Response({"error": "Invalid token: User ID missing."}, status=400)

        # verify if user exists
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return Response({"error": "Invalid token: User does not exist."}, status=401)

        del user['password']
        user['_id'] = str(user['_id'])
        return Response({"message": "Token is valid.", "user": user}, status=200)
    except jwt.InvalidTokenError as e:
        logging.error("Invalid token: %s", e)
        return Response({"error": "Invalid token."}, status=401)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return Response({"error": "An unexpected error occurred."}, status=500)
