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