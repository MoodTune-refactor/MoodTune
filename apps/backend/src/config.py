import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
