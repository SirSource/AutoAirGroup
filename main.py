from flask import Flask, request, redirect, url_for, render_template, session
import stripe
import os

from werkzeug.utils import secure_filename
from utilities.valid import Valid as v
from handler.users import UserHandler as u
from handler.products import ProductsHandler as p
from handler.tax import TaxHandler as t
from handler.staff import StaffHandler as s
from handler.orders import OrdersHandler as o
from handler.passReset import PassResetHandler as pr
from utilities.sendmail import SendMail as mail
import pymongo

stripe_keys = {
    'secret_key': 'sk_test_L1gq9DkWasFWF93WONLDWhUw',
    'publishable_key': 'pk_test_D3JW1FlVygvBQIz2uDJlPHix',
    'live_secret': 'sk_live_829z48QuQMKzuYJ95xjVUUSa',
    'live_pub': 'pk_live_aOGdiL9OkX0PAGcHXf2oMsJp'
}

stripe.api_key = stripe_keys['live_secret']

application = app = Flask(__name__)
app.secret_key = 'PGaxILENXyNhKV3meAMa'
UPLOAD_FOLDER = app.root_path + '/static/img/products/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])


@app.route('/')
def home():
    """
    Routing for home page.
    """
    return render_template('index.html')


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    """
    Routing for catalog page.
    """
    try:
        products = p().getAllProductsCatalog()
        if request.method == 'POST':
            if request.form['_method'] == 'genericsearch':
                # Query items from the generic form.
                products = p().getGenericSearchCatalog(request.form['query'])
                # No results found
                if len(products) == 0:
                    products = 'no_products'
                return render_template('catalog.html', products=products)
            # Advanced search was queried.
            products = p().searchProductsByCar(request.form)
            # No products found.
            if products == None:
                products = 'no_products'
                return render_template('catalog.html', products=products)
            if len(products[1]) == 0:
                products = 'no_products'
                return render_template('catalog.html', products=products)
            else:
                return render_template('catalog.html', products=products[1])
        return render_template('catalog.html', products=products)

    except pymongo.errors.AutoReconnect:
        print("ERRORRRRRRRR")


@app.route('/product/<string:pid>')
def product(pid):
    """
    Routing for product page.
    """
    # Control variable for item existing in cart.
    inCart = False
    operation = p().getProductByID(pid)
    result = operation[0]
    try:
        # Retrieve the product from the variable operation.
        value = operation[1][0]
    except:
        # return to the catalog
        return redirect(url_for('catalog'))
    message = operation[2]
    # Check if item is in cart.
    if 'cart' in session:
        inCart = itemInCart(pid, session['cart'])
    return render_template('product.html', product=value, inCart=inCart)


@app.route('/about')
def about():
    """
    Routing for about the company page.
    """
    return render_template('about.html')


@app.route('/contact')
def contact():
    """
    Routing for contact the company page.
    """
    return render_template('contact.html')


@app.route('/account', methods=['GET', 'POST'])
def accounts():
    """
    Routing for user accounts page.
    """
    if 'email' in session:
        return redirect(url_for('user', email=session['email']))
    message = None
    if request.method == 'POST':
        method = request.form['_method']
        # User requested to log in.
        if method == 'LOG_IN':
            # Authenticate the user from the form.
            operation = u().userAuthenticate(request.form)
            message = operation[2]
            if operation[0]:
                session['email'] = operation[1]
                return redirect(url_for('user', email=operation[1]))
        # user requested to create a new account
        elif method == 'CREATE_USER':
            # Create a new user from the form information.
            operation = u().insertUser(request.form)
            condition = operation[0]
            message = operation[1]
            # If the user could not be created condition == False
            if not condition:
                return render_template('userSession.html', message=message)
            elif condition:
                # user was created, send them email.
                session['email'] = message
                mail().sendAccountCreationEmail(session['email'])
                return redirect(url_for('user', email=message))
    return render_template('userSession.html', message=message)


@app.route('/account/user/<string:email>')
def user(email):
    """
    Routing for user profile page.
    """
    # Check if the user is logged in.
    if 'email' not in session:
        return redirect(url_for('accounts'))
    elif not session['email'] == email:
        email = session['email']
    # Fetch the user from the database.
    user = u().getUserByEmail(email)
    operation = o().getOrdersByEmail(email)
    # Check if user has orders linked to their email address.
    if not operation[0]:
        orders = operation[2]
    else:
        orders = operation[1]
    return render_template('userProfile.html', orders=orders, user=user)


@app.route('/account/user/<string:email>/<string:oid>')
def userOrderReceipt(email, oid):
    """
    Routing for viewing the receipt in the account.
    """
    # Check if user is logged in.
    if 'email' not in session:
        return redirect(url_for('accounts'))
    elif not session['email'] == email:
        email = session['email']
    # Retrieve their orders and render the receipt in html.
    orders = o().getOrdersByOrderID(oid)
    return render_template('receipt.html', order=orders)


@app.route('/order/receipt/confirmation/<string:oid>')
def orderReceipt(oid):
    """
    Routing for viewing the receipt for users with no account or logged off.
    """
    # Retrieve the order
    orders = o().getOrdersByOrderID(oid)
    # If order does not exist, send user to home page.
    if orders == None:
        return redirect(url_for('home'))
    # Render receipt html.
    return render_template('receipt.html', order=orders)


@app.route('/account/user/<string:email>/edit', methods=['GET', 'POST'])
def userEdit(email):
    """
    Routing for user profile editor page.
    """
    # Check if user is logged in.
    if 'email' not in session:
        return redirect(url_for('accounts'))
    elif not session['email'] == email:
        email = session['email']
    message = ''
    # user has submitted a form.
    if request.method == 'POST':
        postType = request.form['_method']
        # User wants to update the address.
        if postType == 'ADD_ADDRESS':
            operation = u().updateUserAddress(email, request.form)
            message = operation[1]
        # User wants to change the password.
        if postType == 'CHANGE_PASSWORD':
            operation = u().updateUserPassword(email, request.form)
            message = operation[1]
    # retrieve the user by looking up the email.
    user = u().getUserByEmail(email)
    return render_template('userProfileEdit.html', user=user, message=message)


@app.route('/logout')
def logout():
    """
    Routing for when the user logs out page.
    """
    # Remove their session.
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/request/password', methods=['GET', 'POST'])
def requestUser():
    """
    Routing for when the user requests a passwor reset.
    """
    # remove the user session if logged in.
    session.pop('email', None)
    if request.method == 'POST':
        # create the reset key and link
        operation = pr().resetPassword(request.form['email'])
        if operation == None:
            return render_template('requestPassword.html', message='failed')
        else:
            # send email to user
            mail().sendAccountRecoverEmail(request.form['email'], pr().getResetFromForms(request.form['email'])[0])
            return render_template('requestPassword.html', message='success')
    return render_template('requestPassword.html')


@app.route('/request/password/staff', methods=['GET', 'POST'])
def requestStaff():
    """
    Routing for when the staff reqeust a password reset.
    """
    # remove the staff from the session.
    session.pop('eid', None)
    if request.method == 'POST':
        # create the reset key and link
        operation = pr().resetPassword(request.form['eid'])
        if operation == None:
            return render_template('requestPasswordStaff.html', message='failed')
        else:
            # Send Email to staff member
            mail().sendAccountRecoverEmail(s().getStaffByEidMain(request.form['eid'])[1]['staff_email'],
                                           pr().getResetFromForms(request.form['eid'])[0])
            return render_template('requestPasswordStaff.html', message='success')
    return render_template('requestPasswordStaff.html')


@app.route('/user/reset/password/<string:key>')
def resetUser(key):
    """
    Routing for when the user accesses a reset link.
    """
    try:
        # Check if user exists and generate a key.
        user = pr().getReset(key)
    except:
        return redirect(url_for('home'))
    # Remove sessions from the user if either staff/admin or regular user.
    session.pop('email', None)
    session.pop('eid', None)
    # User was determined to be a regular user.
    if user[1] == 'user':
        session['email'] = user[0]
        return render_template('userResetPass.html')
    # User was determined to be staff or admin.
    elif user[1] == 'staff':
        session['eid'] = user[0]
        return render_template('staffResetPass.html')


@app.route('/user/reset/password/complete', methods=['POST'])
def resetPassUser():
    """
    Routing for user reset page.
    """
    if not request.method == 'POST':
        session.pop('email', None)
        return redirect(url_for('home'))
    else:
        # Retrieve the user reset key.
        user = u().updateUserPasswordReset(session['email'], request.form)
        message = user[1]
        if message == 'updated_password':
            return redirect(url_for('accounts'))
        else:
            # If user failed to enter an appropriate password, or navigated away from the page, the link will expire.
            session.pop('email', None)
            return render_template('resetFailed.html')


@app.route('/user/reset/password/auth', methods=['POST'])
def resetPassStaff():
    """
    Routing for staff reset page.
    """
    if not request.method == 'POST':
        session.pop('eid', None)
        return redirect(url_for('home'))
    else:
        # Retrieve the staff reset key.
        user = s().updateStaffPasswordReset(session['eid'], request.form)
        message = user[1]
        if message == 'updated_password':
            return redirect(url_for('admin'))
        else:
            # If user failed to enter an appropriate password, or navigated away from the page, the link will expire.
            session.pop('eid', None)
            return render_template('resetFailed.html')


@app.route('/cart')
def cart():
    """
    Routing for shopping cart page.
    """
    # The user has nothing in the cart, senf them to the catalog.
    if 'cart' not in session:
        return render_template('cart.html')
    # Send them for checkout.
    return redirect(url_for('checkout'))


@app.route('/cart/add', methods=['GET', 'POST'])
def cartAdd():
    """
    Routing for adding items to the cart page.
    """
    # If request method is not post, user will be redirected to catalog page.
    if request.method == 'GET':
        return redirect(url_for('catalog'))
    if request.method == 'POST':
        product = request.form['_cartPid']
        qty = request.form['qty']
        # Make sure only one zero was entered in the form.
        if int(qty) + 0 == 0:
            qty = '0'
        # The cart exists and has items.
        if 'cart' in session:
            # The product does not exist. Enter it.
            if not any(product in d for d in session['cart']):
                session['cart'].append({product: qty})
            # The product exists. Update qty.
            elif any(product in d for d in session['cart']):
                for d in session['cart']:
                    d.update((k, qty) for k, v in d.items() if k == product)
        else:
            session['cart'] = [{product: qty}]
    # Get the quantity of items in the cart and store in a session for use in the cart button.
    if len(session['cart']) > 0:
        session['allQty'] = getQtyFromCart(session['cart'])
    # The session was modified
    session['cart'] = purgeEmptyItemFromCart(session['cart'])
    session.modified = True
    return redirect(request.referrer)


@app.route('/checkout')
def checkout():
    """
    Routing for checking out the products purchased.
    """
    user = None
    error = False
    # user has no cart session (empty cart)
    if 'cart' not in session:
        return redirect('catalog')
    # user is logged in.
    if 'email' in session:
        user = u().getUserByEmail(session['email'])
    # Verify there is no error in the cart (item without required quantity).
    if 'cartError' in session:
        error = session['cartError']
        session.pop('cartError', None)
    # Verify if items in cart have a qty of zero, if so remove those items.
    session['cart'] = purgeEmptyItemFromCart(session['cart'])
    # Set the users total quantity.
    session['allQty'] = getQtyFromCart(session['cart'])
    session.modified = True
    # If cart is now empty, return user to catalog.
    if len(session['cart']) == 0:
        session.pop('cart', None)
        session.pop('allQty', None)
        return redirect(url_for('catalog'))
    operation = o().createOrderfromCart(session['cart'])
    return render_template('checkout.html', user=user, products=operation[1], total=operation[2], shipping=operation[3],
                           taxed=operation[4], grandTotal=operation[5], allQty=operation[6], error=error)


@app.route('/process/payment')
def payment(order):
    """
    Routing for page that processes the order.
    """
    oid = order['oid']
    email = order['email']
    zipcode = order['zip']
    total = order['total']
    return render_template('pay.html', email=email, zip=zipcode, total=total)


@app.route('/charge', methods=['POST'])
def charge():
    """
    Routing for a stripe charge.
    """
    # user cannot access this page directly if they try, send them to home page.
    if not request.method == 'POST':
        return redirect(url_for('home'))
    if request.method == 'POST':
        oid = request.form['_oid']
        amount = request.form['_amount']
        email = request.form['_email']
        customer = stripe.Customer.create(
            email=email,
            source=request.form['stripeToken']
        )
        try:
            # Charge the order amount to the user
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency='usd',
                description='Compra Auto Air Group'
            )

            m = mail()
            m.sendOrderConfirmationEmail(email, oid, amount)
        # If payment fails, exception is raised.
        except stripe.error.CardError as e:

            body = e.json_body
            err = body.get('error', {})

            print("Status is: %s" % e.http_status)
            status = e.http_status
            print(status)
            print("Type is: %s" % err.get('type'))
            print("Code is: %s" % err.get('code'))
            # param is '' in this case
            print("Param is: %s" % err.get('param'))
            print("Message is: %s" % err.get('message'))
            # print("CARD ERROR")
            # flash('Error processing payment.', 'error')
            # Set order status to cancelled.
            o().updateOrderStatusToCanceled(oid)
            return render_template('paymentFailed.html')
    # Payment processed correctly, set order to complete.
    o().updateOrderStatusToComplete(oid)
    # Send confirmation email.
    mail().sendOrderConfirmationEmail(email, oid)
    return render_template('succesfulPayment.html')  # Aqui puedes poner algun template como que confirmando o no


@app.route('/checkout/process', methods=['POST'])
def processOrder():
    """
    Routing for processing the order once verified.
    """
    # This page cannot be accessed directly, if so, redirect user to home.
    if request.referrer == None:
        return redirect('/')
    # Create a user from the form information.
    user = u().formToFormattedUser(request.form)
    if request.form['_userStatus'] == '_newUser':
        genericPassword = v().generatePassword()
        None
    order = o().createOrderForProcessing(user[1], session['cart'])
    if not order[0]:
        session['cart'] = removeProductFromCart(order[1], session['cart'])
        session['cartError'] = True
        session.modified = True
        return render_template('cartForced.html')
    session.pop('cart', None)
    session.pop('allQty', None)
    return render_template('pay.html', order=order[1], key=stripe_keys['live_pub'])


@app.route('/tos')
def tos():
    """
    Routing for terms of service page.
    """
    return render_template('tos.html')


@app.route('/privacy')
def privacy():
    """
    Routing for privacy policy page.
    """
    return render_template('privacy.html')


# ---ADMIN PAGES---#
@app.route('/admin')
def admin():
    """
    Routing for admin dashboard.
    """
    # If admin not logged in send to login page.
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    operation = s().staffIsAdmin(session['eid'])
    complete = o().countCompleteOrders()
    pending = o().countPendingOrders()
    unshipped = o().countUnshippedOrders()
    canceled = o().countCanceledOrders()
    actualOrders = o().getAllOrders()
    return render_template('admin.html', complete=complete, pending=pending, unshipped=unshipped, canceled=canceled,
                           staffStatus=operation[1], orders=actualOrders)


@app.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
    """
    Routing for admin login page.
    """
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
    """
    Routing for admin or staff logging out.
    """
    session.pop('eid', None)
    return redirect(url_for('admin'))


@app.route('/admin/staff/account/', methods=['GET', 'POST'])
def staffProfile():
    """
    Routing for staff or admin profile page.
    """
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
    """
    Routing for staff or admin view of orders.
    """
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    message = None
    # Get information about orders by status
    orders = o().getAllOrders()
    complete = o().countCompleteOrders()
    pending = o().countPendingOrders()
    unshipped = o().countUnshippedOrders()
    canceled = o().countCanceledOrders()
    # Search form for orders was engaged.
    if request.method == 'POST':
        method = request.form['_method']
        # Search by phone number.
        if method == 'FIND_PHONE':
            operation = o().getOrdersByPhone(request.form)
            message = operation[2]
            if operation[0]:
                orders = operation[1]
        # Search by order id.
        elif method == 'OID':
            oid = request.form.getlist('orderQuery')
            return adminOrdersView(oid[0])
    staffStatus = s().staffIsAdmin(session['eid'])[1]
    return render_template('adminOrders.html', orders=orders, complete=complete, pending=pending, unshipped=unshipped,
                           canceled=canceled, searchMessage=message, staffStatus=staffStatus)


@app.route('/admin/orders/<string:oid>', methods=['GET', 'POST'])
def adminOrdersView(oid):
    """
    Routing for the admin or staff to view a specific order.
    """
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
    """
    Routing for admin page to view all products.
    """
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
    product = p().getAllProducts()
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
            return render_template('adminProducts.html', products=product, message=operation[2])
        elif method == 'SEARCH':
            product = p().genericProductSearch(request.form['query'])
    return render_template('adminProducts.html', products=product)


@app.route('/admin/products/<string:pid>', methods=['GET', 'POST'])
def adminProductsView(pid):
    """
    Routing for admin to view a particular product and edit it.
    """
    if 'eid' not in session:
        return redirect(url_for('adminLogin'))
    staffStatus = s().staffIsAdmin(session['eid'])[0]
    if not staffStatus:
        return redirect(url_for('admin'))
    operation = p().getProductByID(pid)
    product = operation[1]
    if not operation[0]:
        return render_template('adminProductView.html', product=None)
    if request.method == 'POST':
        # It will have the same picture
        if 'file' not in request.files:
            # EDIT PRODUCT WITHOUT PHOTO
            operation = p().EditProductByID(None, request.form)
            product = p().getProductByID(pid)[1]  # devuelve una lista de una lista del producto
            return render_template('adminProductView.html', productExist=operation[0], product=product[0], pid=pid)
        else:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                extension = filename.split('.')
                image = v().generatePhotoName(extension[1])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
                operation = p().EditProductByID(image, request.form)
                product = p().getProductByID(pid)[1]  # devuelve una lista de una lista del producto
            return render_template('adminProductView.html', productExist=operation[0], product=product[0], pid=pid)

    return render_template('adminProductView.html', productExist=operation[0], product=product[0], pid=pid)


@app.route('/admin/tax', methods=['GET', 'POST'])
def adminTax():
    """
    Routing for admin to set sales tax.
    """
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
    """
    Routing admin to create and view staff.
    """
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
            staff = s().genericStaffSearch(request.form['eid'])
            message = 'employee_found'
            if len(staff) == 0:
                message = 'no_staff'
            return render_template('adminStaff.html', message=message, staff=staff)
        if method == 'DELETE':
            if session['eid'] == request.form['eid']:
                return render_template('adminStaff.html', deleteStatus='delete_error_self', staff=s().getAllStaff())
            operation = s().deleteStaff(request.form)
            return render_template('adminStaff.html', deleteStatus=operation[1], staff=s().getAllStaff())
    return render_template('adminStaff.html', staff=staff)


@app.route('/admin/staff/<string:eid>', methods=['GET', 'POST'])
def adminStaffEdit(eid):
    """
    Routing editing elements of the staff page.
    """
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
    """
    Redirects to the 404 error page
    """
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    """
    Redirects to the 403 error page
    """
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    """
    Redirects to the 500 error page
    """
    return render_template('500.html'), 500


# Upload functions
def allowed_file(filename):
    """
    Verifies that an image file to be uploaded complies with the permitted file types.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Cart purge orders with zero quantity
def purgeEmptyItemFromCart(cart):
    """
    If the cart has items with qty = 0, they are removed.
    :param cart: All items in the cart
    :return: A new cart without the items with qty = 0
    """
    for x in cart:
        pid = list(x.keys())[0]
        qty = x[pid]
        if qty == '0':
            cart.remove(x)
    return cart


# Get the total qty of items in the cart
def getQtyFromCart(cart):
    """
    Retreives the total qty of items in the cart.
    :param cart: The cart se session.
    :return: The total qty of items in the cart.
    """
    qty = 0
    for x in cart:
        pid = list(x.keys())[0]
        qty = qty + int(x[pid])
    return qty


def removeProductFromCart(pid, cart):
    """
    Removes a particular product from the cart.
    :param pid: The id of the product to remove.
    :param cart: The cart session from the user.
    :return: A new cart without the particular product.
    """
    for x in cart:
        product = list(x.keys())[0]
        if pid == product:
            cart.remove(x)
    return cart


def itemInCart(pid, cart):
    """
    Checks if a particular item is in the cart already.
    :param pid: The id of the product.
    :param cart: The cart session from the user.
    :return: True if the item is in tha cart, False otherwise.
    """
    for x in cart:
        product = list(x.keys())[0]
        if pid == product:
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
