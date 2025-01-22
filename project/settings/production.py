from .base import *

DEBUG = False
ALLOWED_HOSTS = ['api.lexiai.hdcola.org', 'lexiai.hdcola.org']

DATABASES = {
    'mdb': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('DB_NAME'),
        'CLIENT': {
            'host': os.environ.get('MONGO_URI')
        }
    }
}
