"""
Django settings for SaveYourPage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# BASE_DIR = '/Users/air13/Desktop/SaveYourPage/'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l7$1vuurgj9!d-9do*oqu^1z@6xm1t+#v3t6fbbgg7ve=%57hq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
    "/Users/air13/Desktop/SaveYourPage/templates",
)

# STATICFILES_DIRS = (
#     '/Users/air13/Desktop/SaveYourPage/static'
# )
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'app',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
#     'PAGINATE_BY': 10
# }

ROOT_URLCONF = 'SaveYourPage.urls'

WSGI_APPLICATION = 'SaveYourPage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'saveyourpage',
        'USER': 'root',
        'PASSWORD': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
