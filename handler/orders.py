import datetime
from dao.orders import OrdersDao
from handler.products import ProductsHandler as p
from utilities.valid import Valid as v
from bson.decimal128 import Decimal128
from handler.tax import TaxHandler as t


class OrdersHandler:

    def order_dictionary(self, row):
        address = row['address']
        del row['address']
        del row['_id']
        result = {**address, **row}
        return result

    def getAllOrders(self):
        dao = OrdersDao()
        list = dao.getAllOrders()
        result_list = []
        for row in list:
            result = self.order_dictionary(row)
            result_list.append(result)
        return result_list

    def getOrdersByOrderID(self, oid):
        if self.orderExists(oid):
            dao = OrdersDao()
            item = dao.getOrdersByOrderID(oid)
            return self.order_dictionary(item)
        else:
            return None

    def getOrdersByEmail(self, email):
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
        if self.orderExists(oid):
            OrdersDao().deleteOrderById(oid)
            return True
        else:
            return False

    def deleteOrderByUserEmail(self, email):
        if self.emailOrderExists(email):
            OrdersDao().deleteOrderByUserEmail(email)
            return True
        else:
            return False

    def updateOrderStatusForm(self, oid, form):
        status = form['payment_status']
        if status == 'pending':
            OrdersDao().updateOrderStatusForm(oid, status)
            return True, 'order_pending'
        elif status == 'complete':
            OrdersDao().updateOrderStatusForm(oid, status)
            return True, 'order_complete'
        elif status == 'canceled':
            OrdersDao().updateOrderStatusForm(oid, status)
            return True, 'order_canceled'
        else:
            return False, 'update_error'

    def updateOrderShippingForm(self, oid, form):
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
        products = []
        shipping = Decimal128('0')
        ivu = Decimal128(str(t().getTax()))
        total = Decimal128('0')
        for item in cart:
            pid = list(item.keys())[0]
            query = p().getProductByID(pid)[1][0]
            pprice = query['pprice']
            pshipping = query['pshipping']
            qty = Decimal128(item[pid])
            newProduct = {
                'pid': pid,
                'pname': query['pname'],
                'plocation': query['plocation'],
                'qty': item[pid],
                'unit_price': pprice,
                'unit_total': Decimal128(pprice.to_decimal() * qty.to_decimal())
            }
            products.append(newProduct)
            total = Decimal128(total.to_decimal() + (pprice.to_decimal() * qty.to_decimal()))
            shipping = Decimal128(shipping.to_decimal() + query['pshipping'].to_decimal())
        taxed = Decimal128(ivu.to_decimal() * total.to_decimal())
        grandTotal = Decimal128(total.to_decimal() + taxed.to_decimal())
        return True, products, total, shipping, taxed, grandTotal, 'cart_exists'

    def cartToDisplay(self, cart):
        products = []
        shipping = 0
        # TODO: Check quantities, make sure valid. Place PID of quantity that failed in a list.
        for item in cart:
            pid = list(item.keys())[0]
            query = p().getProductByID(pid)[1][0]
            newProduct = {
                'pid': pid,
                'pname': query['pname'],
                'plocation': query['plocation'],
                'qty': item[pid],
                'unit_price': query['pprice'],
                'unit_total': query['pprice'] * int(item[pid])
            }
            print(newProduct)
            products.append(newProduct)
            shipping = shipping + query['pshipping']
        oid = self.generateOrderNumber()
        date = datetime.datetime.now()
        return True, products, shipping, 'cart_exists'

    def generateOrderNumber(self):
        sequence = OrdersDao().getOrderSequenceNumber()
        sequence = sequence + 1
        OrdersDao().updateOrderSequenceNumber(sequence)
        return sequence

    # ---Auxiliary Methods---#

    def orderExists(self, oid):
        order = OrdersDao().getOrdersByOrderID(oid)
        if order == None:
            return False
        else:
            return True

    def emailOrderExists(self, email):
        order = OrdersDao().getOrdersByEmail(email)
        if order == None:
            return False
        else:
            return True

    def countCompleteOrders(self):
        return OrdersDao().countCompleteOrders()

    def countPendingOrders(self):
        return OrdersDao().countPendingOrders()

    def countCanceledOrders(self):
        return OrdersDao().countCanceledOrders()

    def countUnshippedOrders(self):
        return OrdersDao().countUnshippedOrders()
