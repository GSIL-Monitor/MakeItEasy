from makeiteasy.settings.base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'makeitaesy',
        'USER': 'jerry',
        'PASSWORD': 'edx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),'staticfiles')
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles'),
