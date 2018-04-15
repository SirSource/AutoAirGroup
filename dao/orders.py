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
        allOrders = []
        orders = self.db
        for doc in orders.find({"orderid": iod}):
            allOrders.append(doc)
        return allOrders

    def getOrdersByEmail(self, email):
        allOrders = []
        orders = self.db
        for doc in orders.find({"uemail": email}):
            allOrders.append(doc)
        return allOrders

    def getOrdersByStatus(self, status):
        allOrders = []
        orders = self.db
        for doc in orders.find({"payment_status": status}):
            allOrders.append(doc)
        return allOrders

    def getOrdersShipped(self):
        allOrders = []
        orders = self.db
        for doc in orders.find({"shipping": "shipped"}):
            allOrders.append(doc)
        return allOrders

    #TODO: Add more functions for getters, inserts, and deletes