from flask import Flask, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from utilities.valid import Valid as v
from handler.users import UserHandler as u
from handler.products import ProductsHandler as p
from handler.tax import TaxHandler as t
from handler.staff import StaffHandler as s
from handler.orders import OrdersHandler as o

app = Flask(__name__)

UPLOAD_FOLDER = app.root_path + '/static/img/products/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

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
    pending = o().countPendingOrders()
    unshipped = o().countUnshippedOrders()
    canceled = o().countCanceledOrders()
    return render_template('adminOrders.html', orders=orders, complete=complete, pending=pending, unshipped=unshipped,
                           canceled=canceled)


@app.route('/admin/orders/<string:oid>', methods=['GET', 'POST'])
def adminOrdersView(oid):
    order = o().getOrdersByOrderID(oid)
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'UPDATE_STATUS':
            o().updateOrderStatusForm(oid, request.form)
            order = o().getOrdersByOrderID(oid)
        elif method == 'UPDATE_SHIPPING':
            o().updateOrderShippingForm(oid, request.form)
            order = o().getOrdersByOrderID(oid)
    if order == None:
        return render_template('adminOrdersView.html', order=None, oid=oid)
    else:
        return render_template('adminOrdersView.html', order=order, oid=oid)


@app.route('/admin/products', methods=['GET', 'POST'])
def adminProducts():
    if request.method == 'POST':
        method = request.form['_method']
        print(request.form)
        if method == 'ADD_PRODUCT':
            if 'file' not in request.files:
                operation = p().addProduct('', request.form)
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                extension = filename.split('.')
                image = v().generatePhotoName(extension[1])
                print(image)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
                operation = p().addProduct(image, request.form)
                product = operation[1]
                message = operation[2]
    return render_template('adminProducts.html', products=p().getAllProducts())

@app.route('/admin/products/<string:pid>', methods=['GET', 'POST'])
def adminProductsView(pid):
    operation = p().getProductByID(pid)
    product = operation[1]
    return render_template('adminProductView.html', productExist=operation[0], product=product[0], pid=pid)

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
            return render_template('adminStaff.html', addSuccess=operation[1], staff=s().getAllStaff())
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
            return render_template('adminStaff.html', deleteStatus=operation[1], staff=s().getAllStaff())
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


# Upload functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
