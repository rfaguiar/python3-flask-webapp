import os

# for item, value in os.environ.items():
#     print('{}: {}'.format(item, value))
	
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = os.environ.get('MYSQL_DB')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT'))

SECRET_KEY = "secret_jogoteca"
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
