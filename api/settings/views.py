import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..authentication import JWTAuthentication
from pymongo import MongoClient
from bson import ObjectId


client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db['users']


class SettingsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token_user = request.user.user
            user_id = token_user['_id']
            user = users_collection.find_one({"_id": ObjectId(user_id)})

            if not user:
                return Response({"error": "Invalid token: User does not exist."}, status=401)

            # safely retrieve the `settings` field
            settings = user.get('settings', None)
            if settings is not None:
                return Response({"settings": settings}, status=200)
            else:
                return Response({"result": "null"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # set the settings for the current user
        try:
            token_user = request.user.user
            user_id = token_user['_id']
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return Response({"error": "Invalid token: User does not exist."}, status=401)

            settings_data = request.data.get('settings', {})
            user['settings'] = settings_data
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"settings": settings_data}}
            )
            return Response({"settings": settings_data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # update the settings for the current user
        try:
            token_user = request.user.user
            user_id = token_user['_id']
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return Response({"error": "Invalid token: User does not exist."}, status=401)

            # If settings is not present, initialize it
            settings = user.get('settings', {})
            if 'settings' not in user:
                user['settings'] = {}  # initialize empty settings 

            settings_data = request.data.get('settings', {})

            user['settings'].update(settings_data)
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"settings": user['settings']}}
            )
            return Response({"settings": user['settings']}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
