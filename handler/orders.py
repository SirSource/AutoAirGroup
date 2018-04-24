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
        dao = OrdersDao()
        item = dao.getOrdersByOrderID(oid)
        if item == None:
            return None
        return self.order_dictionary(item)

    def getOrdersByEmail(self, email):
        dao = OrdersDao()
        item = dao.getOrdersByEmail(email)
        if item == None:
            return None
        return self.order_dictionary(item)

    def getOrdersByStatus(self, status):
        dao = OrdersDao()
        item = dao.getOrdersByStatus(status)
        if item == None:
            return None
        return self.order_dictionary(item)

    def getOrdersShipped(self):
        dao = OrdersDao()
        item = dao.getOrdersShipped()
        if item == None:
            return None
        return self.order_dictionary(item)

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

    #---Auxiliary Methods---#

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