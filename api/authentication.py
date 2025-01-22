import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization', None)
        if not token:
            return None

        try:
            payload = jwt.decode(token.split(
                ' ')[1], settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(username=payload['username'])
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
        'id': str(user['_id']),
        'exp': datetime.now() + timedelta(days=1),  # 1-day expiration
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
