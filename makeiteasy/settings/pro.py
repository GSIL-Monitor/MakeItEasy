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

# log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'errorfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/error.log'),
        },
        'infofile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/info.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['errorfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'makeiteasy': {
            'handlers': ['infofile'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
