"""
Django settings for rincart project.
"""

from pathlib import Path
import os
import environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Environment variables Initialize ചെയ്യുക
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'rincart.onrender.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    
    # 👈 കൃത്യമായ ഓർഡർ: staticfiles-ന് മുകളിലായിരിക്കണം ഇത്!
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    
    'rincartapp',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'anymail',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'rincart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rincart.wsgi.application'

# Neon Connection configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript)
# 1. പഴയ STORAGES ഡിക്ഷ്ണറിയും STATICFILES_STORAGE-ഉം പൂർണ്ണമായി ഒഴിവാക്കി ഇത് മാത്രം നൽകുക:
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # WhiteNoise-ൽ വരാവുന്ന ഫയൽ മിസ്സിങ് എററുകൾ ഒഴിവാക്കാൻ ഇതാണ് കറക്റ്റ് വഴി:
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# 👈 ഈ വരി നിർബന്ധമായും തൊട്ടുതാഴെ ചേർക്കുക (ഇതാണ് മെയിൻ സൊല്യൂഷൻ)
WHITENOISE_MANIFEST_STRICT = False


# 2. 'cloudinary_storage' പാക്കേജിന് വേണ്ടി ഈ ഒരു വരി നിർബന്ധമായും ചേർക്കുക:
# ഇത് ചേർക്കുമ്പോഴാണ് അപ്ലിക്കേഷൻ ക്രാഷ് ആകാതിരിക്കുന്നത്
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# 3. ബാക്കി മീഡിയ സെറ്റിങ്സ് താഴെ പറയുന്ന രീതിയിൽ നിലനിർത്തുക
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'odmzdqtb',
    'API_KEY': '621758957527618',
    'API_SECRET': 'mPFKmYvXioCdRaNqZMhZwa1Scnc',
}


# Social Account configurations
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_ADAPTER = 'rincartapp.adapters.MySocialAccountAdapter'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_SIGNUP_REDIRECT_URL = '/verify-otp/'
LOGIN_REDIRECT_URL = '/verify-otp/'

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
DEFAULT_FROM_EMAIL = "RinCart Official <rincartofficial@gmail.com>"
ANYMAIL = {
    "BREVO_API_KEY": env("BREVO_API_KEY"),
}
