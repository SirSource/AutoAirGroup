import datetime
from dao.orders import OrdersDao
from handler.products import ProductsHandler as p
from utilities.valid import Valid as v
from bson.decimal128 import Decimal128
from handler.tax import TaxHandler as t
from decimal import Decimal


class OrdersHandler:

    def order_dictionary(self, row):
        """
        Convert raw information from the database into a list of orders.
        :param row: Database information
        :return: List of orders
        """
        address = row['address']
        del row['address']
        del row['_id']
        result = {**address, **row}
        return result

    def getAllOrders(self):
        """
        Fetch all orders from the database
        :return: A list of all orders
        """
        dao = OrdersDao()
        list = dao.getAllOrders()
        result_list = []
        for row in list:
            result = self.order_dictionary(row)
            result_list.append(result)
        return result_list

    def getOrdersByOrderID(self, oid):
        """
        Retrieve an order by the ID
        :param oid: Id of order to find
        :return: The order with matching ID
        """
        try:
            # try to fetch the order
            if self.orderExists(oid):
                dao = OrdersDao()
                item = dao.getOrdersByOrderID(oid)
                return self.order_dictionary(item)
            else:
                return None
        except:
            return None

    def getOrdersByEmail(self, email):
        """
        Fetch order by customer email address.
        :param email: Customer email
        :return: All matching orders
        """
        dao = OrdersDao()
        item = dao.getOrdersByEmail(email)
        if item == None:
            return False, None, 'no_orders'
        result_list = []
        for row in item:
            result = self.order_dictionary(row)
            result_list.append(result)
        return True, result_list, 'orders_exist'

    def getOrdersByPhone(self, form):
        """
        Fetch orders by customer phone
        :param form: Customer phone number in form.
        :return: List of matching orders.
        """
        phone = form['orderQuery']
        if not v().validPhone(phone):
            return False, None, 'invalid_phone'
        dao = OrdersDao()
        item = dao.getOrdersByPhone(phone)
        if item == None:
            return False, None, 'no_orders'
        result_list = []
        for row in item:
            result = self.order_dictionary(row)
            result_list.append(result)
        return True, result_list, 'orders_exist'

    def getOrdersByStatus(self, status):
        """
        Fetch all orders that match a status
        :param status: The status to search
        :return: Matching orders as a list.
        """
        dao = OrdersDao()
        item = dao.getOrdersByStatus(status)
        if item == None:
            return False, None, 'no_orders'
        result_list = []
        for row in item:
            result = self.order_dictionary(row)
            result_list.append(result)
        return True, result_list, 'orders_exist'

    def getOrdersShipped(self):
        """
        Fetch orders that are marked as shipped.
        :return: All orders matching shipped status.
        """
        dao = OrdersDao()
        item = dao.getOrdersShipped()
        if item == None:
            return False, None, 'no_orders'
        result_list = []
        for row in item:
            result = self.order_dictionary(row)
            result_list.append(result)
        return True, result_list, 'orders_exist'

    def deleteOrderById(self, oid):
        """
        Delete an order by it's ID
        :param oid:
        :return: True if deleted, False if not
        """
        if self.orderExists(oid):
            OrdersDao().deleteOrderById(oid)
            return True
        else:
            return False

    def deleteOrderByUserEmail(self, email):
        """
        Delete an order by user email
        :param email: The email of the user tied to the order
        :return: True if deleted, false if not
        """
        if self.emailOrderExists(email):
            OrdersDao().deleteOrderByUserEmail(email)
            return True
        else:
            return False

    def updateOrderStatusForm(self, oid, form):
        """
        Process a form to update the payment status
        :param oid: Id of order
        :param form: Form inputted by the user.
        :return: Boolean and message for front end
        """
        status = form['payment_status']
        if status == 'pending':
            OrdersDao().updateOrderStatusForm(oid, status)
            return True, 'order_pending'
        elif status == 'complete':
            OrdersDao().updateOrderStatusForm(oid, status)
            return True, 'order_complete'
        elif status == 'canceled':
            self.updateOrderStatusToCanceled(oid)
            return True, 'order_canceled'
        else:
            return False, 'update_error'

    def updateOrderStatusToComplete(self, oid):
        """
        Set status of order to complete.
        :param oid: Id of order
        """
        OrdersDao().updateOrderStatusForm(oid, 'complete')

    def updateOrderStatusToCanceled(self, oid):
        """
        Set status of order to cancel.
        :param oid: Id of order
        """
        order = self.getOrdersByOrderID(oid)
        if not (order['payment_status'] == 'canceled'):
            # Loop through products and return to inventory.
            for product in order['products']:
                p().increaseProductQty(product['pid'], (int(product['qty'])))
            OrdersDao().updateOrderStatusForm(oid, 'canceled')

    def updateOrderShippingForm(self, oid, form):
        """
        Update the shipping status from a form.
        :param oid: Id of orcer
        :param form: Form with information
        :return: Boolean, Message for front end.
        """
        status = form['shipping_status']
        if status == 'shipped':
            OrdersDao().updateOrderShippingForm(oid, status)
            return True, 'order_shipped'
        elif status == 'not_shipped':
            OrdersDao().updateOrderShippingForm(oid, status)
            return True, 'order_not_shipped'
        else:
            return False, 'update_error'

    def createOrderfromCart(self, cart):
        """
        Create an order from the items in the shopping cart to display during checkout.
        :param cart: The user's cart session.
        :return: Boolean, products list, total, shipping, grand total, total qty and message for front end.
        """
        # set empty variables for processing
        products = []
        shipping = Decimal128('0')
        ivu = Decimal128(str(t().getTax()))
        total = Decimal128('0')
        allQty = Decimal128('0')
        # loop through individual cart items.
        for item in cart:
            pid = list(item.keys())[0]
            qty = Decimal128(item[pid])
            query = p().getProductByID(pid)[1][0]
            pprice = query['pprice']
            pshipping = query['pshipping']
            allQty = Decimal128(allQty.to_decimal() + qty.to_decimal())
            newProduct = {
                'pid': pid,
                'pname': query['pname'],
                'plocation': query['plocation'],
                'qty': item[pid],
                'unit_price': pprice,
                'unit_total': Decimal128(pprice.to_decimal() * qty.to_decimal())
            }
            # Add products to list.
            products.append(newProduct)
            total = Decimal128(round(total.to_decimal() + (pprice.to_decimal() * qty.to_decimal()), 2))
            shipping = Decimal128(
                round(shipping.to_decimal() + (qty.to_decimal() * query['pshipping'].to_decimal()), 2))
        # Calculate totals and tax.
        roundedTax = round(ivu.to_decimal() * total.to_decimal(), 2)
        taxed = Decimal128(roundedTax)
        grandTotal = Decimal128(total.to_decimal() + taxed.to_decimal() + shipping.to_decimal())
        shipping = self.shippingCalcPercentage(shipping, allQty)
        return True, products, total, shipping, taxed, grandTotal, allQty, 'cart_exists'

    def createOrderForProcessing(self, user, cart):
        """
        Create the order for processing payment via stripe.
        :param user: The user that placed the order.
        :param cart: The user's cart session.
        :return: Boolean, ID if failed, None db connection problem, or the processed order.
        """
        # set empty variables for processing
        products = []
        shipping = Decimal128('0')
        ivu = Decimal128(str(t().getTax()))
        total = Decimal128('0')
        allQty = Decimal128('0')
        # loop through individual cart items.
        for item in cart:
            pid = list(item.keys())[0]
            qty = Decimal128(item[pid])
            query = p().getProductByID(pid)[1][0]
            pprice = query['pprice']
            pshipping = query['pshipping']
            allQty = Decimal128(allQty.to_decimal() + qty.to_decimal())
            newProduct = {
                'pid': pid,
                'pname': query['pname'],
                'plocation': query['plocation'],
                'qty': item[pid],
                'unit_price': pprice,
                'unit_total': Decimal128(pprice.to_decimal() * qty.to_decimal())
            }
            # Add products to list.
            products.append(newProduct)
            total = Decimal128(total.to_decimal() + (pprice.to_decimal() * qty.to_decimal()))
            shipping = Decimal128(shipping.to_decimal() + query['pshipping'].to_decimal())
            # Verify product quantities in inventory.
            if p().productQtyAvailable(pid, int(item[pid])):
                p().decreaseProductQty(pid, int(item[pid]))
            else:
                return False, pid
        # Calculate totals and tax.
        roundedTax = round(ivu.to_decimal() * total.to_decimal(), 2)
        taxed = Decimal128(roundedTax)
        grandTotal = Decimal128(total.to_decimal() + taxed.to_decimal() + shipping.to_decimal())
        shipping = self.shippingCalcPercentage(shipping, allQty)
        oid = self.generateOrderNumber()
        date = datetime.datetime.now()
        dao = OrdersDao()
        theOrder = dao.insertOrder(oid, user, total, ivu, taxed, grandTotal, shipping, date, products)
        if theOrder[0] == False:
            return False, None
        returnOrder = {
            'oid': oid,
            'email': user['uemail'],
            'total': int(grandTotal.to_decimal() * 100),
            'zip': user['zipcode']
        }
        return True, returnOrder

    def generateOrderNumber(self):
        """
        Generate order numbers from the following current one in the database
        :return: The generated number
        """
        sequence = OrdersDao().getOrderSequenceNumber()
        sequence = sequence + 1
        OrdersDao().updateOrderSequenceNumber(sequence)
        return sequence

    # ---Auxiliary Methods---#

    def orderExists(self, oid):
        """
        Check if order exists.
        :param oid: Order ID
        :return: True if exists False if not.
        """
        order = OrdersDao().getOrdersByOrderID(oid)
        if order == None:
            return False
        else:
            return True

    def emailOrderExists(self, email):
        """
        Check if order exists from user email.
        :param oid: Email of user
        :return: True if exists False if not.
        """
        order = OrdersDao().getOrdersByEmail(email)
        if order == None:
            return False
        else:
            return True

    def countCompleteOrders(self):
        """
        Count the number of complete orders in the system
        :return: Total
        """
        return OrdersDao().countCompleteOrders()

    def countPendingOrders(self):
        """
        Count the number of pending orders in the system
        :return: Total
        """
        return OrdersDao().countPendingOrders()

    def countCanceledOrders(self):
        """
        Count the number of canceled orders in the system
        :return: Total
        """
        return OrdersDao().countCanceledOrders()

    def countUnshippedOrders(self):
        """
        Count the number of unshipped orders in the system
        :return: Total
        """
        return OrdersDao().countUnshippedOrders()

    def shippingCalcPercentage(self, shipping, qty):
        """
        Calculate shipping charges based upon total items in the cart.
        :param shipping: Current total shipping.
        :param qty: Total items in cart.
        :return: New shipping price
        """
        qty = int(str(qty))
        twoToFour = Decimal128('0.9')
        fiveToSeven = Decimal128('0.8')
        eightToNine = Decimal128('0.7')
        tenPlus = Decimal128('0.6')
        if qty >= 2 and qty <= 4:
            return Decimal128(round((shipping.to_decimal() * twoToFour.to_decimal()), 2))
        if qty >= 5 and qty <= 7:
            return Decimal128(round((shipping.to_decimal() * fiveToSeven.to_decimal()), 2))
        if qty >= 8 and qty <= 9:
            return Decimal128(round((shipping.to_decimal() * eightToNine.to_decimal()), 2))
        if qty >= 10:
            return Decimal128(round((shipping.to_decimal() * tenPlus.to_decimal()), 2))
        return shipping

    def shippingCalcFixed(self, shipping):
        """
        Cap the shipping price to a fixed amount.
        :param shipping:
        :return:
        """
        testShipping = float(str(shipping))
        if testShipping > 50:
            return Decimal128('50.00')
        return shipping
