from config.dbconfig import client


class OrdersDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.orders

    def getAllOrders(self):
        allOrders = []
        orders = self.db
        for doc in orders.find():
            allOrders.append(doc)
        return allOrders

    def getOrdersByOrderID(self, iod):
        order = self.db.find_one({"orderid": iod})
        return order

    def getOrdersByEmail(self, email):
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"uemail": email}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def getOrdersByStatus(self, status):
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"payment_status": status}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def getOrdersShipped(self):
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"shipping": "shipped"}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def deleteOrderById(self, oID):
        return self.db.delete_many({"orderid": oID})

    def deleteOrderByUserEmail(self, email):
        return self.db.delete_many({"uemail": email})

    # TODO: Add more functions for getters, inserts, and deletes
