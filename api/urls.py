from django.urls import path
from .views import register_user, test_user

urlpatterns = [
    path('users/register', register_user, name='register_user'),
    path('users/test', test_user, name='test_user')
]