from config import PROJECT_HOME
from os import path

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "football-manager"
#SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/tracks.db'
#SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
#SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

USE_S3 = True

USE_RDS = False
DB_PATH = path.join(PROJECT_HOME, 'data/msia423.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False