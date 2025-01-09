import os
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.conf import settings

mongo_uri = os.getenv('MONGO_URI')

client = MongoClient(mongo_uri)
db = client['DB_NAME']
users_collection = db['users']

@api_view(['POST'])
def create_user(request):
    data = request.data

    user_data = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],
        'createdAt': datetime.datetime.now(), 
    }

    users_collection.insert_one(user_data)

    return Response({'message': 'User created successfully'})

