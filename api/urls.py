from django.urls import path

from .settings.views import SettingsView
from .favorites.views import FavoritesView
from .views import register_user, login_user, get_all_languages, get_language_by_id, get_topics_for_level, get_all_ai_styles, get_ai_style_by_id, validate_jwt

urlpatterns = [
    path('users/register', register_user, name='register_user'),
    path('users/login', login_user, name='login_user'),
    path('jwt/validate', validate_jwt, name='validate_jwt'),
    path('languages', get_all_languages, name='get_all_languages'),
    path('languages/<str:id>', get_language_by_id, name='get_language_by_id'),
    path('topics', get_topics_for_level, name='get_topics_for_level'),
    path('styles', get_all_ai_styles, name='get_all_ai_styles'),
    path('styles/<str:id>', get_ai_style_by_id, name='get_ai_style_by_id'),
    path('users/settings', SettingsView.as_view(), name='settings'),
    path('users/favorites', FavoritesView.as_view(), name='favorites'),
]
