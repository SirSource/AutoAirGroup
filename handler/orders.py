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
        try:
            if self.orderExists(oid):
                dao = OrdersDao()
                item = dao.getOrdersByOrderID(oid)
                return self.order_dictionary(item)
            else:
                return None
        except:
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
            self.updateOrderStatusToCanceled(oid)
            return True, 'order_canceled'
        else:
            return False, 'update_error'

    def updateOrderStatusToComplete(self, oid):
        OrdersDao().updateOrderStatusForm(oid, 'complete')

    def updateOrderStatusToCanceled(self, oid):
        order = self.getOrdersByOrderID(oid)
        if not(order['payment_status']=='canceled'):
            for product in order['products']:
                p().increaseProductQty(product['pid'],(int(product['qty'])))
            OrdersDao().updateOrderStatusForm(oid, 'canceled')


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
        allQty = Decimal128('0')
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
            products.append(newProduct)
            total = Decimal128(total.to_decimal() + (pprice.to_decimal() * qty.to_decimal()))
            shipping = Decimal128(shipping.to_decimal() + query['pshipping'].to_decimal())
        roundedTax = round(ivu.to_decimal() * total.to_decimal(), 2)
        taxed = Decimal128(roundedTax)
        grandTotal = Decimal128(total.to_decimal() + taxed.to_decimal() + shipping.to_decimal())
        return True, products, total, shipping, taxed, grandTotal, allQty, 'cart_exists'

    def createOrderForProcessing(self, user, cart):
        products = []
        shipping = Decimal128('0')
        ivu = Decimal128(str(t().getTax()))
        total = Decimal128('0')
        allQty = Decimal128('0')
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
            products.append(newProduct)
            total = Decimal128(total.to_decimal() + (pprice.to_decimal() * qty.to_decimal()))
            shipping = Decimal128(shipping.to_decimal() + query['pshipping'].to_decimal())
            if p().productQtyAvailable(pid, int(item[pid])):
                p().decreaseProductQty(pid, int(item[pid]))
            else:
                return False, pid
        roundedTax = round(ivu.to_decimal() * total.to_decimal(), 2)
        taxed = Decimal128(roundedTax)
        grandTotal = Decimal128(total.to_decimal() + taxed.to_decimal() + shipping.to_decimal())
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
