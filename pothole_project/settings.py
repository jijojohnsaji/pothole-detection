from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-i3ay3jt&4int4^sra=lb$oj)s4!0iwuau(y=-9)4ft-t+81j@%'
DEBUG = True
ALLOWED_HOSTS = []


# =========================
# Installed Apps
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'detection.apps.DetectionConfig',
    'users.apps.UsersConfig',
]


# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================
# URL / WSGI
# =========================
ROOT_URLCONF = 'pothole_project.urls'
WSGI_APPLICATION = 'pothole_project.wsgi.application'


# =========================
# Templates
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =========================
# Database
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# Password Validation
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]


# =========================
# Internationalization
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =========================
# Static Files
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]


# =========================
# Default Primary Key
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# Authentication Redirects
# =========================
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/detection/route-map/'
LOGOUT_REDIRECT_URL = '/users/login/'


# =========================
# Email Configuration
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Replace with your Gmail
EMAIL_HOST_USER = 'enteramail@gmail.com'

# Replace with your Gmail App Password
EMAIL_HOST_PASSWORD = 'enter-gmail-paaword'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER