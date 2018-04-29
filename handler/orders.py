from dao.orders import OrdersDao


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
        if self.emailOrderExists(email):
            dao = OrdersDao()
            item = dao.getOrdersByEmail(email)
            result_list = []
            for row in item:
                result = self.order_dictionary(row)
                result_list.append(result)
            return result_list
        else:
            return None

    def getOrdersByStatus(self, status):
        dao = OrdersDao()
        item = dao.getOrdersByStatus(status)
        if item == None:
            return False
        result_list = []
        for row in item:
            result = self.order_dictionary(row)
            result_list.append(result)
        return result_list

    def getOrdersShipped(self):
        dao = OrdersDao()
        item = dao.getOrdersShipped()
        if item == None:
            return False
        result_list = []
        for row in item:
            result = self.order_dictionary(row)
            result_list.append(result)
        return result_list

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

    def countCanceledOrders(self):
        return OrdersDao().countCanceledOrders()

    def countUnshippedOrders(self):
        return OrdersDao().countUnshippedOrders()
