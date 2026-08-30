"""
Django settings for plumbing_site project — Robert Evan's Plumbing & Electrician.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'dev-only-secret-key-change-this-before-deploying-5f8s7d6f5s4d6f5'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local apps
    'accounts',
    'core',
    'messaging',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plumbing_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'messaging.context_processors.unread_counts',
                'core.context_processors.business_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'plumbing_site.wsgi.application'
ASGI_APPLICATION = 'plumbing_site.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---- Auth / accounts ----
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'messaging:dashboard_redirect'
LOGOUT_REDIRECT_URL = 'core:home'

# Business info, surfaced in templates via context processor
BUSINESS = {
    'name': "Robert Evan's Plumbing & Electrician",
    'tagline': "Powering homes & fixing flows.",
    'phone': '(555) 019-4477',
    'messenger': 'Robert Evan\'s plumbing and electrician',
    'hours': '24/7 Emergency Service',
    'followers': '275',
}

# ---- Web Push notifications ----
# Lets a logged-in user get a phone/desktop notification (with sound, via the
# OS) the instant a message is sent to them — even if the site isn't open.
# Real key pair is committed for local/dev use; override both via env vars
# for production so your own server holds the private key.
VAPID_PUBLIC_KEY = os.environ.get(
    'VAPID_PUBLIC_KEY',
    'BBLKyn5KToZQoc8wkl1EjpSU8QdOQKPuAVkvkJjtH9inGprHfXDAJzehVOkDPQN7XeHh-KAPQjQNAJaupeqMlsM',
)
VAPID_PRIVATE_KEY_PATH = os.environ.get(
    'VAPID_PRIVATE_KEY_PATH', str(BASE_DIR / 'vapid_private_key.pem')
)
VAPID_CLAIMS_EMAIL = os.environ.get(
    'VAPID_CLAIMS_EMAIL', 'mailto:admin@robertevans-plumbing.example'
)

