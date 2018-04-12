from flask import Flask
from config.dbconfig import client

app = Flask(__name__)
#mongo = PyMongo(app)

##TEST SNIPPET
from dao.users import UsersDao
call = UsersDao().getAllUsers()
insert = UsersDao().insertUser()
##END OF TEST SNIPPET

@app.route('/')
def test():
    return

if __name__ == '__main__':
    app.run(debug=True)