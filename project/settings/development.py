from .base import *

# updated just for testing purposes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mdb': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('DB_NAME'),
        'CLIENT': {
            'host': os.environ.get('MONGO_URI')
        }
    }
}
