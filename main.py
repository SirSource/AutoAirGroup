from flask import Flask
from config.dbconfig import client

app = Flask(__name__)
#mongo = PyMongo(app)

@app.route('/')
def test():
    ##TEST SNIPPET
    from dao.users import UsersDao
    get = UsersDao().getUserByEmail("jdp@gmail.com")
    ##END OF TEST SNIPPET
    return

if __name__ == '__main__':
    app.run(debug=True)