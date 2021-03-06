# Python imports
from os.path import join

# project imports
from .common import *

# uncomment the following line to include i18n
from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# adjust the minimal login
#LOGIN_URL = 'core_login'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'
#LOGOUT_REDIRECT_URL = 'core_login'

# Per una autenticazione personalizzata (via email e non username)
AUTH_USER_MODEL = 'users.CustomUser'


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS
