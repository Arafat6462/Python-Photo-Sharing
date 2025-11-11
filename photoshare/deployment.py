import os
from settings import *

SECRET_KEY = os.environ['SECRET'] # Set in Azure App Settings
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] # Azure sets this environment variable. 
CSRF_TRUSTED_ORIGINS = [f"https://{os.environ['WEBSITE_HOSTNAME']}"] # For CSRF protection
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # Optimize static file serving
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Directory for collectstatic


# Database configuration for Azure
connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
if connection_string:
    conn_params = {param.split('=')[0]: param.split('=')[1] for param in connection_string.split()}

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': conn_params['dbname'],
            'USER': conn_params['user'],
            'PASSWORD': conn_params['password'],
            'HOST': conn_params['host'],
            'PORT': conn_params.get('port', 5432),
            'OPTIONS': {
                'sslmode': 'require'
            }
        }
    }
else:
    print("AZURE_POSTGRESQL_CONNECTIONSTRING environment variable not found. Using default database settings.")
    # The DATABASES from settings.py will be used
    pass