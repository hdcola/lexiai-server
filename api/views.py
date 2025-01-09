import os
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')

client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db['users']


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