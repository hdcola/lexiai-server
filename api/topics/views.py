import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..authentication import JWTAuthentication
from pymongo import MongoClient
from bson import json_util

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db['users']
topics_collection = db['topics']

pipeline = [
    {
        "$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user_info"
        }
    },
    {
        "$unwind": {                    # explode the user_info array
            "path": "$user_info",
            "preserveNullAndEmptyArrays": True  # if user_info is empty, keep the document
        }
    },
    {
        "$project": {
            "_id": 1,
            "title": 1,
            "description": 1,
            "level": 1,
            "systemPrompt": 1,
            "start": 1,
            "createdAt": 1,
            "user_id": 1,
            "user_info._id": 1,
            "user_info.username": 1,
            "user_info.email": 1,
            "user_info.createdAt": 1
        }
    }
]


class TopicsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        level = request.query_params.get('level', None)
        try:
            if level is None:
                topics = list(topics_collection.aggregate(pipeline))
            else:
                matching = {
                    "$match": {"level": level}
                }
                topics = list(topics_collection.aggregate(
                    [matching] + pipeline))

            return Response({"topics": parse_json(topics)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def parse_json(data):
    return json.loads(json_util.dumps(data))
