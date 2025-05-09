"""
Django settings for Ecogo_2025 project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import json
from django.utils.html import format_html

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
####datos de configuración
ruta= os.path.dirname(os.path.abspath(__file__))
f = open('{}/conf.json'.format(ruta), 'r')
conf_string = f.read()
f.close()
conf = json.loads(conf_string)

BASE_URL=conf['base_url']


# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s9t!*l*nb03y3!3=92hc1w=70_3jm^zuo$n4_h1x_pypyb!g#+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ecogo.cl','127.0.0.1','149.50.130.61']

INTERNAL_IPS = [
    "127.0.0.1",
]

#NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
NPM_BIN_PATH = "/usr/bin/npm" 
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'home',
    'alumno',
    'docente',
    'coordinador',
    'acceso',
    'inventario',
    'tailwind',
    'theme' ,
    'django_browser_reload',
    'crispy_forms',
    'crispy_tailwind',
    'widget_tweaks',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'Ecogo_2025.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Ecogo_2025.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
        
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')

#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecogo_db',
        'USER': 'eco_admin',#admin
        'PASSWORD': conf["password"],
        'HOST': conf['server'],  # O la IP del servidor de MySQL
        'PORT': '3306',  # Puerto predeterminado de MySQL
        'OPTIONS': {
            'charset': 'utf8mb4',

        },
    }
}


# settings.py
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": conf["DATABASE_NAME"],
#         "USER": conf["DATABASE_USER"],
#         "PASSWORD": conf["DATABASE_PASSWORD"],
#         "HOST": conf["DATABASE_HOST"],
#         "PORT": conf["DATABASE_PORT"],
        
#     }
# }



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

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




#STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



JAZZMIN_UI_TWEAKS = {
    "theme": "cerulean",
}

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Admin Ecogo",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Admin Ecogo",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Ecogo Backend",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "/images/elementos gráficos/logo-iniciar-sesion.webp",
    
    "site_logo_classes": "img-circle",
    #"welcome_sign": format_html("<img src='/images/elementos gráficos/logo-iniciar-sesion.webp'>"),
    "copyright": "Desarrollado por Escuela de Turismo y Hospitalidad de Duoc UC- Sede Valparaíso ",
    "show_sidebar": True,
    "changeform_format": "horizontal_tabs",
    "user_avatar": None,

    
}


CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"
TAILWIND_APP_NAME = 'theme'
