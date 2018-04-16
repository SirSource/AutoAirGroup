from flask import Flask, render_template
from handler.users import UserHandler as u
from handler.products import ProductsHandler as p

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/accounts')
def accounts():
    return render_template('userSession.html')

@app.route('/users')
def getAllUsers():
    return u().getAllUsers()

if __name__ == '__main__':
    app.run(debug=True)