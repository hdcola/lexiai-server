from django.urls import path
from .views import register_user, login_user, get_all_languages, get_topics_for_level, get_all_ai_styles

urlpatterns = [
    path('users/register', register_user, name='register_user'),
    path('users/login', login_user, name='login_user'),
    path('languages', get_all_languages, name='get_all_languages'),
    path('topics', get_topics_for_level, name='get_topics_for_level'),
    path('styles', get_all_ai_styles, name='get_all_ai_styles')
]