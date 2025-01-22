import json
from bson import ObjectId, json_util
from pymongo import MongoClient
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..authentication import JWTAuthentication

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')

client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['users']
topics_collection = db['topics']


class FavoritesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token_user = request.user.user
            user_id = token_user['_id']
            user = users_collection.find_one({"_id": ObjectId(user_id)})

            if not user:
                return Response({"error": "Invalid token: User does not exist."}, status=401)

            # safely retrieve the `favorites` field
            settings = user.get('settings', None)

            if settings is not None:
                favorites = settings.get('favorites', None)
                if favorites is not None:
                    topics = []
                    for key, value in favorites.items():
                        if value:
                            # retrieve the topic from the database
                            topic = topics_collection.find_one(
                                {"_id": ObjectId(key)})
                            if topic:
                                # add the topic to the favorites
                                topics.append(topic)

                    return Response({"favorites": parse_json(topics)}, status=200)

            return Response({"favorites": "{}"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # update the favorites for the current user
        try:
            token_user = request.user.user
            user_id = token_user['_id']
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return Response({"error": "Invalid token: User does not exist."}, status=401)
            settings = user.get('settings', None)
            if settings is None:
                user['settings'] = {'favorites': {}}
            favorites = user['settings'].get('favorites', None)
            if favorites is None:
                user['settings']['favorites'] = {}
                favorites = user['settings']['favorites']

            favorites_data = request.data.get('favorites', {})
            # for each favorites_data key, update the user's favorites
            for key, value in favorites_data.items():
                if value:
                    # if value is True, add the key to the user's favorites
                    favorites[key] = True
                else:
                    # if value is False, remove the key from the user's favorites
                    favorites.pop(key, None)
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"settings.favorites": favorites}}
            )
            return Response({"favorites": favorites}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def parse_json(data):
    return json.loads(json_util.dumps(data))
