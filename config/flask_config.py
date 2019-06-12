from config import PROJECT_HOME
from os import path

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
APP_NAME = "football-manager"

PORT = 3000
HOST = "127.0.0.1"
MAX_ROWS_SHOW = 100

USE_S3 = False
USE_RDS = True
DATABASE_NAME = 'msia423'
DB_PATH = path.join(PROJECT_HOME, 'data/msia423.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False