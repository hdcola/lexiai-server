from django.urls import path
from .views import register_user, get_all_languages, get_topics_for_level, get_all_ai_styles
from .ai import text_to_text, text_to_speech

urlpatterns = [
    path('users/register', register_user, name='register_user'),
    path('text', text_to_text, name='text_to_text'),
    path('speech', text_to_speech, name='text_to_speech'),
    path('languages', get_all_languages, name='get_all_languages'),
    path('topics', get_topics_for_level, name='get_topics_for_level'),
    path('styles', get_all_ai_styles, name='get_all_ai_styles')
]