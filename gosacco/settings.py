
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ertyuiop4345679809-0--lkjhgvc'  # Add secret in local_settings.py

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'django.contrib.sites',
    'polymorphic',
    'corsheaders',
    'gosacco',
    'members',
    'loans',
    'savings',
    'shares',
    'fees',
    'debug_toolbar',
    'notifications',
)

SITE_ID = 1
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'gosacco.urls'

WSGI_APPLICATION = 'gosacco.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:5000',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

    ),
    #'DEFAULT_PERMISSION_CLASSES': ('members.permissions.IsOwner',),
}


JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'gosacco.account_utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=60),
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),


}

STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'info': {
        'contact': 'mark@lubegamark.com',
        'description': 'This is the API for GoSacco. ',
        # 'license': 'Apache 2.0',
        # 'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        # 'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'GoSacco API',
    },
    'doc_expansion': 'none',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR + '/emails/'


# All secrets should be added from the local_settings.py that's not added to source control
try:
    from local_settings import *
except:
    pass
