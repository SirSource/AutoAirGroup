from flask import Flask, request, render_template
from handler.users import UserHandler as u
from handler.products import ProductsHandler as p
from handler.tax import TaxHandler as t
from handler.staff import StaffHandler as s

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    products = p().getAllProducts()
    return render_template('catalog.html', products = products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/accounts')
def accounts():
    return render_template('userSession.html')

@app.route('/users')
def getAllUsers():
    return u().getAllUsers()

#---ADMIN PAGES---#
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/orders')
def adminOrders():
    return render_template('adminOrders.html')

@app.route('/admin/products')
def adminProducts():
    products = p().getAllProducts()
    return render_template('adminProducts.html', products = products)

@app.route('/admin/tax', methods=['GET','POST'])
def adminTax():
    value = True
    if request.method == 'POST':
        value = t().setTax(request.form.getlist('tax'))
    tax = t().getTax()
    return render_template('adminTax.html', fee = tax, value = value)

@app.route('/admin/staff', methods=['GET','POST'])
def adminStaff():
    staff = s().getAllStaff()
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'ADD':
            addSuccess = s().insertStaff(request.form)
            if addSuccess:
                return render_template('adminStaff.html', addSuccess = 'pass', staff = staff)
            else:
                return render_template('adminStaff.html', addSuccess = 'fail', staff = staff)
        if method == 'SEARCH':
            None
        if method == 'DELETE':
            None
    return render_template('adminStaff.html', staff = staff)


if __name__ == '__main__':
    app.run(debug=True)