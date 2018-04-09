import os

SECRET_KEY = "secret_jogoteca"
MYSQL_HOST = "0.0.0.0"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "jogoteca"
MYSQL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'