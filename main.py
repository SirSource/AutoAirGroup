from flask import Flask, request, redirect, url_for, render_template, session
import os
from werkzeug.utils import secure_filename
from utilities.valid import Valid as v
from handler.users import UserHandler as u
from handler.products import ProductsHandler as p
from handler.tax import TaxHandler as t
from handler.staff import StaffHandler as s
from handler.orders import OrdersHandler as o

app = Flask(__name__)
app.secret_key = 'PGaxILENXyNhKV3meAMa'
UPLOAD_FOLDER = app.root_path + '/static/img/products/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    products = p().getAllProducts()
    if request.method == 'POST':
        products = p().searchProductsByCar(request.form)
        if len(products[1]) == 0:
            products = 'no_products'
            return render_template('catalog.html', products=products)
        else:
            return render_template('catalog.html', products=products[1])
    return render_template('catalog.html', products=products)


@app.route('/product/<string:pid>')
def product(pid):
    operation = p().getProductByID(pid)
    result = operation[0]
    value = operation[1][0]
    message = operation[2]
    return render_template('product.html', product=value)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/account', methods=['GET', 'POST'])
def accounts():
    if 'email' in session:
        return redirect(url_for('user', email=session['email']))
    message = None
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'LOG_IN':
            operation = u().userAuthenticate(request.form)
            message = operation[2]
            if operation[0]:
                session['email'] = operation[1]
                return redirect(url_for('user', email=operation[1]))
        elif method == 'CREATE_USER':
            operation = u().insertUser(request.form)
            condition = operation[0]
            message = operation[1]
            if not condition:
                return render_template('userSession.html', message=message)
            elif condition:
                session['email'] = message
                return redirect(url_for('user', email=message))
    return render_template('userSession.html', message=message)


@app.route('/account/user/<string:email>')
def user(email):
    if 'email' not in session:
        return redirect(url_for('accounts'))
    elif not session['email'] == email:
        email = session['email']
    user = u().getUserByEmail(email)
    operation = o().getOrdersByEmail(email)
    if not operation[0]:
        orders = operation[2]
    else:
        orders = operation[1]
    return render_template('userProfile.html', orders=orders, user=user)


@app.route('/account/user/<string:email>/edit', methods=['GET', 'POST'])
def userEdit(email):
    if 'email' not in session:
        return redirect(url_for('accounts'))
    elif not session['email'] == email:
        email = session['email']
    if request.method == 'POST':
        postType = request.form['_method']
        if postType == 'ADD_ADDRESS':
            operation = u().updateUserAddress(email, request.form)
        if postType == 'CHANGE_PASSWORD':
            operation = u().updateUserPassword(email, request.form)
    user = u().getUserByEmail(email)
    return render_template('userProfileEdit.html', user=user)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/cart/add', methods=['GET', 'POST'])
def cartAdd():
    if request.method == 'POST':
        product = request.form['_cartPid']
        qty = request.form['qty']
        print(str(product) + " " + str(qty))
        if 'cart' in session:
            if not any(product in d for d in session['cart']):
                session['cart'].append({product: qty})
            elif any(product in d for d in session['cart']):
                for d in session['cart']:
                    d.update((k, qty) for k, v in d.items() if k == product)
        else:
            session['cart'] = [{product: qty}]
        print(session['cart'])
    session.modified = True
    return redirect(request.referrer)


@app.route('/checkout')
def checkout():
    user = None
    if 'cart' not in session:
        return redirect('catalog')
    if 'email' in session:
        user = u().getUserByEmail(session['email'])
    session['cart'] = purgeEmptyItemFromCart(session['cart'])
    session.modified = True
    operation = o().createOrderfromCart(session['cart'])
    return render_template('checkout.html', user=user, products=operation[1], total=operation[2], shipping=operation[3],
                           taxed=operation[4], grandTotal=operation[5], allQty=operation[6])


@app.route('/checkout/process', methods=['POST'])
def processOrder():
    if request.referrer == None:
        return redirect('/')
    user = u().formToFormattedUser(request.form)
    print(request.form)
    if request.form['_userStatus'] == '_newUser':
        print('HERE')
        genericPassword = v().generatePassword()
        print(genericPassword)
        None
    order = o().createOrderForProcessing(user[1], session['cart'])
    print(order)
    session.pop('cart', None)
    return redirect('/')


@app.route('/users')
def getAllUsers():
    return u().getAllUsers()


# ---ADMIN PAGES---#
@app.route('/admin')
def admin():
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    operation = s().staffIsAdmin(session['eid'])
    complete = o().countCompleteOrders()
    pending = o().countPendingOrders()
    unshipped = o().countUnshippedOrders()
    canceled = o().countCanceledOrders()
    return render_template('admin.html', complete=complete, pending=pending, unshipped=unshipped, canceled=canceled,
                           staffStatus=operation[1])


@app.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
    session.pop('email', None)
    if 'eid' in session:
        adminOp = s().staffIsAdmin(session['eid'])
        return redirect(url_for('admin'))
    if request.method == 'POST':
        operation = s().staffAuthenticate(request.form)
        result = operation[0]
        eid = operation[1]
        message = operation[2]
        if result:
            session['eid'] = eid
            adminOp = s().staffIsAdmin(session['eid'])
            return redirect(url_for('admin'))
    return render_template('adminLogin.html')


@app.route('/admin/endsession')
def staffEndSession():
    session.pop('eid', None)
    return redirect(url_for('admin'))


@app.route('/admin/staff/account/', methods=['GET', 'POST'])
def staffProfile():
    message = None
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'UPDATE_PASS':
            eid = request.form['eid']
            operation = s().updateStaffPassword(eid, request.form['oldPass'], request.form['newPass'])
            message = operation[1]
            print(message)
    eid = session['eid']
    admin = s().staffIsAdmin(session['eid'])[0]
    staff = s().getStaffByEidMain(eid)[1]
    return render_template('staffProfile.html', admin=admin, staff=staff, updateStatus=message)


@app.route('/admin/orders', methods=['GET', 'POST'])
def adminOrders():
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    message = None
    orders = o().getAllOrders()
    complete = o().countCompleteOrders()
    pending = o().countPendingOrders()
    unshipped = o().countUnshippedOrders()
    canceled = o().countCanceledOrders()
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'FIND_PHONE':
            operation = o().getOrdersByPhone(request.form)
            message = operation[2]
            print(operation[2])
            if operation[0]:
                orders = operation[1]
        elif method == 'OID':
            oid = request.form.getlist('orderQuery')
            return adminOrdersView(oid[0])
    staffStatus = s().staffIsAdmin(session['eid'])[1]
    return render_template('adminOrders.html', orders=orders, complete=complete, pending=pending, unshipped=unshipped,
                           canceled=canceled, searchMessage=message, staffStatus=staffStatus)


@app.route('/admin/orders/<string:oid>', methods=['GET', 'POST'])
def adminOrdersView(oid):
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[1]
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
        return render_template('adminOrdersView.html', order=None, oid=oid, staffStatus=staffStatus)
    else:
        return render_template('adminOrdersView.html', order=order, oid=oid, staffStatus=staffStatus)


@app.route('/admin/products', methods=['GET', 'POST'])
def adminProducts():
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        method = request.form['_method']
        if method == 'ADD_PRODUCT':
            if 'file' not in request.files:
                operation = p().addProduct('', request.form)
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                extension = filename.split('.')
                image = v().generatePhotoName(extension[1])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
                operation = p().addProduct(image, request.form)
                product = operation[1]
                message = operation[2]
    return render_template('adminProducts.html', products=p().getAllProducts())


@app.route('/admin/products/<string:pid>', methods=['GET', 'POST'])
def adminProductsView(pid):
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
    operation = p().getProductByID(pid)
    product = operation[1]
    if not operation[0]:
        return render_template('adminProductView.html', product=None)
    return render_template('adminProductView.html', productExist=operation[0], product=product[0], pid=pid)


@app.route('/admin/tax', methods=['GET', 'POST'])
def adminTax():
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
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
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
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
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
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


# Cart purge orders with zero quantity
def purgeEmptyItemFromCart(cart):
    for x in cart:
        pid = list(x.keys())[0]
        qty = x[pid]
        if qty == '0':
            cart.remove(x)
    return cart


if __name__ == '__main__':
    app.run(debug=True)
