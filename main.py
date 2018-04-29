from flask import Flask, request, render_template
from handler.users import UserHandler as u
from handler.products import ProductsHandler as p
from handler.tax import TaxHandler as t
from handler.staff import StaffHandler as s
from handler.orders import OrdersHandler as o

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/catalog')
def catalog():
    products = p().getAllProducts()
    return render_template('catalog.html', products=products)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/accounts')
def accounts():
    return render_template('userSession.html')


@app.route('/users')
def getAllUsers():
    return u().getAllUsers()


# ---ADMIN PAGES---#
@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/admin/orders')
def adminOrders():
    orders = o().getAllOrders()
    complete = o().countCompleteOrders()
    unshipped = o().countUnshippedOrders()
    canceled = o().countCanceledOrders()
    return render_template('adminOrders.html', orders=orders, complete=complete, unshipped=unshipped, canceled=canceled)


@app.route('/admin/orders/<string:oid>')
def adminOrdersView(oid):
    order = o().getOrdersByOrderID(oid)
    if order == None:
        return render_template('adminOrdersView.html', order=None, oid=oid)
    else:
        print(order)
        return render_template('adminOrdersView.html', order=order, oid=oid)


@app.route('/admin/products')
def adminProducts():
    products = p().getAllProducts()
    return render_template('adminProducts.html', products=products)


@app.route('/admin/tax', methods=['GET', 'POST'])
def adminTax():
    tax = t().getTax()
    message = None
    if request.method == 'POST':
        query = t().setTax(request.form.getlist('tax'))
        value = query[0]
        message = query[1]
        if value:
            tax = query[2]
    return render_template('adminTax.html', fee=tax, message=message)


@app.route('/admin/staff', methods=['GET', 'POST'])
def adminStaff():
    staff = s().getAllStaff()
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'ADD':
            operation = s().insertStaff(request.form)
            return render_template('adminStaff.html', addSuccess=operation[1], staff=staff)
        if method == 'SEARCH':
            operation = s().getStaffByEid(request.form)
            status = operation[0]
            result = operation[1]
            message = operation[2]
            if not status:
                return render_template('adminStaff.html', message=message, staff=staff)
            else:
                return render_template('adminStaffEdit.html', staff=result)
        if method == 'DELETE':
            operation = s().deleteStaff(request.form)
            return render_template('adminStaff.html', deleteStatus=operation[1], staff=staff)
    return render_template('adminStaff.html', staff=staff)


@app.route('/admin/staff/<string:eid>', methods=['GET', 'POST'])
def adminStaffEdit(eid):
    operation = s().getStaffByEidMain(eid)
    staff = operation[1]
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'UPDATE_STORE':
            newOperation = s().updateStaffStore(eid, request.form)
            operation = s().getStaffByEidMain(eid)
            staff = operation[1]
            return render_template('adminStaffEdit.html', staff=staff)
        elif method == 'UPDATE_ADMIN':
            newOperation = s().updateStaffAsAdmin(eid, request.form)
            operation = s().getStaffByEidMain(eid)
            staff = operation[1]
            return render_template('adminStaffEdit.html', staff=staff)
    return render_template('adminStaffEdit.html', staff=staff)


# === ERROR HANDLING === #
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
