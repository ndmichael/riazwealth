from pathlib import Path
import environ

# Initialise environment 
env = environ.Env()
environ.Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [
    "localhost", 
    "127.0.0.1", 
    "riazvest-production-0a0f.up.railway.app"
    "riazvest.com",
    "www.riazvest.com"
]

# Application definition

INSTALLED_APPS = [
    # dev created apps
    'investments',
    'users',
    'admin_portal',
    'pages',
    'accounts',
    'referrals',
    'withdrawals',
    'notifications',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "crispy_forms",
    "crispy_bootstrap5",

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    "allauth.socialaccount",
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # set celery beat
    'django_celery_beat',

    # anymail
    'anymail',
    'google_translate',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # allauth 
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
                # `allauth` 
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

print(f"environment: {ENVIRONMENT} env: {env('ENVIRONMENT')}")

if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('NAME'),
            'USER': env('USER') ,
            'PASSWORD': env('PASSWORD') ,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
elif ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'railway',
            'URL': env('DATABASE_URL'),
            'USER': env('PGUSER'),
            'PASSWORD': env('PGPASSWORD'),
            'HOST': env('PGHOST'),
            'PORT': env('PGPORT'),
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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = Path(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'

MEDIA_ROOT = Path(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.CustomUser"

# overriden forms
ACCOUNT_FORMS = {
    "signup": "accounts.forms.MyCustomSignupForm",
    "login": "accounts.forms.MyCustomLoginForm",
}

# auth backend allauth and django
AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",  # Allauth authentication
    "django.contrib.auth.backends.ModelBackend",  # Default Django authentication
]

# Setups for allauth
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
# ACCOUNT_RATE_LIMITS = 7
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "index"

# Ensure username is required
ACCOUNT_USERNAME_REQUIRED = True

# Ensure email is required
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_RATE_LIMITS = {
    # 'section_name': ('num_requests', 'time_period'),
    'login_failed': "5/600s",  # 5 attempts per 600 seconds (10 minutes)
}

# or any other page
LOGIN_REDIRECT_URL = 'user_dashboard'
ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"
ACCOUNT_LOGIN_ON_SIGNUP = False
ACCOUNT_SIGNUP_REDIRECT_URL = "account_login"

# RESEND SETUP
# settings.py
ACCOUNT_ADAPTER = "accounts.adapters.AccountAdapter"
DEFAULT_FROM_EMAIL = "noreply@riazvest.com"
RESEND_API_KEY = env("RESEND_API_KEY")
EMAIL_TIMEOUT = 10

# no EMAIL_HOST*, no EMAIL_BACKEND


# Use Resend backend
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# EMAIL_HOST = "smtp.resend.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = "noreply@riazvest.com"
# EMAIL_HOST_PASSWORD = env("RESEND_API_KEY")

# # Optional email defaults
# DEFAULT_FROM_EMAIL = "noreply@riazvest.com"
# SERVER_EMAIL = "support@riazvest.com"

ACCOUNT_EMAIL_HTML_EMAIL = True




# For stock market predictions
ALPHA_VANTAGE_API_KEY = env("ALPHA_VANTAGE_API_KEY")


# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Change this to Railway Redis URL in production
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'



SITE_URL = "http://127.0.0.1:8000"

# Trusted Origin
CSRF_TRUSTED_ORIGINS = [
    'https://riazvest-production.up.railway.app',
    'https://riazvest.com'
]

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": env('REDIS_URL'),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,  # Important: Make sure this is False 
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         '': {  # Root logger
#             'handlers': ['console'],
#             'level': 'DEBUG', # Set to a suitable level (DEBUG for development)
#         },
#     },
# } 