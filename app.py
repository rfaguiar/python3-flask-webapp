from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MySQL(app)


from views import *

@app.route('/hello')
def hello_world():
    return 'Hello World 2!'

if __name__ == '__main__':
    app.run()
