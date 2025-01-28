import datetime
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..authentication import JWTAuthentication
from pymongo import MongoClient
from bson import ObjectId, json_util

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db['users']
topics_collection = db['topics']

admin_id = ObjectId("678ea72a7baff5011c1a27cf")
# admin_id = ObjectId("67898feecd698cdf88c785f8") # for testing 'anna' user

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
            "system_prompt": 1,
            "start": 1,
            "created_at": 1,
            "user_id": 1,
            "user_info.username": 1,
            "user_info.email": 1
        }
    }
]


class TopicsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_all(self, request):
        level = request.query_params.get('level', None)
        query_user_id = request.query_params.get('user_id', None)
        token_user = request.user.user
        user_id = ObjectId(token_user['_id'])
        try:
            matching = {"$match": {}}
            if query_user_id is not None:
                if query_user_id == "me":
                    matching["$match"]["user_id"] = user_id
                else:
                    matching["$match"]["user_id"] = ObjectId(query_user_id)
            elif level is None:
                matching = {
                    "$match": {
                        "user_id": {"$in": [admin_id]}
                    }
                }
            elif level == "Custom":
                matching = {
                    "$match": {
                        "user_id": {"$in": [user_id]}
                    }
                }
            else:
                matching = {
                    "$match": {
                        "level": level,
                        "user_id": {"$in": [admin_id]}
                    }
                }

            topics = list(topics_collection.aggregate(
                [matching] + pipeline))

            return Response(parse_json(topics), status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, topic_id=None):
        if topic_id is None:
            return self.get_all(request)
        try:
            if topic_id is None:
                return Response({"error": "Topic ID not provided"}, status=400)
            topic = topics_collection.find_one({"_id": ObjectId(topic_id)})
            if not topic:
                return Response({"error": "Topic not found"}, status=404)
            return Response({"topic": parse_json(topic)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        token_user = request.user.user
        user_id = ObjectId(token_user['_id'])
        try:
            topic_data = request.data
            topic_data['user_id'] = user_id
            topic_data['title'] = topic_data.get('title', "")
            topic_data['description'] = topic_data.get('description', "")
            topic_data['level'] = topic_data.get('level', "beginner")
            topic_data['system_prompt'] = topic_data.get('system_prompt', "")
            topic_data['start'] = topic_data.get('start', "")
            topic_data['created_at'] = datetime.datetime.now().strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            topic_id = topics_collection.insert_one(topic_data).inserted_id
            topic = topics_collection.find_one({"_id": topic_id})
            return Response({"topic": parse_json(topic)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, topic_id):
        token_user = request.user.user
        user_id = ObjectId(token_user['_id'])
        try:
            topic_data = request.data
            print("test", topic_data)
            if topic_id is None:
                return Response({"error": "Topic ID not provided"}, status=400)
            topic = topics_collection.find_one({"_id": ObjectId(topic_id)})
            if not topic:
                return Response({"error": "Topic not found"}, status=404)
            if topic['user_id'] != user_id:
                return Response({"error": "Unauthorized"}, status=401)
            topics_collection.update_one(
                {"_id": ObjectId(topic_id)},
                {"$set": topic_data}
            )
            updated_topic = topics_collection.find_one(
                {"_id": ObjectId(topic_id)})
            return Response({"topic": parse_json(updated_topic)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, topic_id):
        token_user = request.user.user
        user_id = ObjectId(token_user['_id'])
        try:
            if topic_id is None:
                return Response({"error": "Topic ID not provided"}, status=400)
            topic = topics_collection.find_one({"_id": ObjectId(topic_id)})
            if not topic:
                return Response({"error": "Topic not found"}, status=404)
            if topic['user_id'] != user_id:
                return Response({"error": "Unauthorized"}, status=401)
            topics_collection.delete_one({"_id": ObjectId(topic_id)})
            return Response({"result": "success"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def parse_json(data):
    return json.loads(json_util.dumps(data))
