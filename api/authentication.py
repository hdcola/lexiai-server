
import os
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import User
from rest_framework import authentication, exceptions
from pymongo import MongoClient
from bson import ObjectId


client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db['users']


class ManualUser:
    def __init__(self, user):
        self.user = user

    @property
    def is_authenticated(self):
        return True


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization', None)
        if not token:
            return None

        try:
            payload = jwt.decode(token.split(
                ' ')[1], settings.TOKEN_KEY, algorithms=['HS256'])
            dbuser = users_collection.find_one(
                {"_id": ObjectId(payload['user_id'])})
            del dbuser['password']
            user = ManualUser(dbuser)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('token is expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('token is invalid')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('user not found')


def generate_jwt(user):
    payload = {
        'email': user['email'],
        'username': user['username'],
        'user_id': str(user['_id']),
        'exp': datetime.now() + timedelta(days=1),  # 1-day expiration
    }
    token = jwt.encode(payload, settings.TOKEN_KEY, algorithm='HS256')
    return token
