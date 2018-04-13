from flask import Flask
from handler.users import UserHandler
from config.dbconfig import client

app = Flask(__name__)
#mongo = PyMongo(app)

@app.route('/')
def greeting():
    return '<h1>Auto Air Group</h1>'

@app.route('/users')
def getAllUsers():
    return UserHandler().getAllUsers()

if __name__ == '__main__':
    app.run(debug=True)