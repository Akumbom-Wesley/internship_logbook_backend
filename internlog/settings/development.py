from .base import *

# Debug settings
DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 300

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1', '192.168.1.142']
