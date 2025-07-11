"""
Django settings for chartwise project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from django.conf import settings
from django.conf.urls.static import static
from datetime import timedelta
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cr5!)u&1n&)417!l^eko8&u!ay=m&qr=*_n1j9auhqcc+r6fjw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STATIC_URL = '/static/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'core',
    'django_rest_passwordreset',
    'ckeditor',
    'captcha',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'chartwise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chartwise.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chartwise_db', 
        'USER': 'andreineagoe23',          
        'PASSWORD': 'Loredana123$',        
        'HOST': 'localhost',
        'PORT': '3306',                     
    }
    
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


from datetime import timedelta

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  
    "https://andreineagoe23.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://kind-gently-ostrich.ngrok-free.app",
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-requested-with',
    'accept',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-xsrf-token',
    'cache-control',
    'pragma',
]

CORS_EXPOSE_HEADERS = ["Content-Disposition"]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': 'auto',
        'extraPlugins': 'uploadimage',
        'filebrowserUploadUrl': '/ckeditor/upload/',
    },
}


CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
# Celery Settings
CELERY_BROKER_URL = 'redis://localhost:6380/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# For periodic tasks, use Django-Celery-Beat
INSTALLED_APPS += ['django_celery_beat']

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/monevocredentials.json")

DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID", "monevo-443011")
CSE_ID = os.getenv("CSE_ID", "")
API_KEY = os.getenv("API_KEY", "")


RECRAFT_API_KEY = os.getenv("RECRAFT_API_KEY")

# reCAPTCHA Settings
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "6Lf5LkArAAAAAKby1cInCi-_nyqedOhkdpSRdt1c")  # Site key
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "6Lf5LkArAAAAACxZWqApBjNz59FBxWhoQ6UEOyR_")  # Secret key
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'neagoeandrei23@gmail.com'
EMAIL_HOST_PASSWORD = 'bzas jnyj mmkx ehtx'
DEFAULT_FROM_EMAIL = 'neagoeandrei23@gmail.com'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'kind-gently-ostrich.ngrok-free.app',
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://andreineagoe23.github.io",
    "http://localhost:8080",
]

CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False  # Must be False to allow JavaScript to read it
CSRF_COOKIE_SAMESITE = 'Lax'  # or 'None' with secure

# settings.py
STRIPE_SECRET_KEY = 'sk_test_51R9kpVBi8QnQXyouk2SS209GQnsf1expP071qhuR9wWghoP9wppWF5URCTJlDXMmyILvF6YwIOCj7CqPULr4maZk004R9iNUA9' 
STRIPE_PUBLISHABLE_KEY = 'pk_test_51R9kpVBi8QnQXyouGcNBa6MYmRUSxTA5xtmzC62r31bVSyelmgspwVE4f1DC7YdUmaOgi8aykHNPSciUm0HLE1Io00aaHBT8O3' 
FRONTEND_URL = "http://localhost:3000"

HF_API_KEY = os.getenv("HF_API_KEY")

import sys

# Switch to SQLite for local test runs to avoid MySQL permission or data issues
if 'test' in sys.argv:
    print("⚠️ Using SQLite for local testing (in-memory)...")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # You can also use BASE_DIR / 'test_db.sqlite3' if needed
        }
    }
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

print("🔑 HF_API_KEY Loaded:", os.getenv("HF_API_KEY"))

# Celery Beat Settings
CELERY_BEAT_SCHEDULE = {
    'send-email-reminders': {
        'task': 'core.tasks.send_email_reminders',
        'schedule': 3600.0,  # Run every hour
    },
}
