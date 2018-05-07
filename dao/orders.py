from config.dbconfig import client
from bson.objectid import ObjectId


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

    def getOrdersByPhone(self, phone):
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"uphone": phone}):
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

    def createOrder(self):
        None

    def updateOrderStatusForm(self, oid, status):
        return self.db.update({'orderid': oid}, {'$set': {'payment_status': status}})

    def updateOrderShippingForm(self, oid, status):
        return self.db.update({'orderid': oid}, {'$set': {'shipping': status}})

    def deleteOrderById(self, oID):
        return self.db.delete_many({"orderid": oID})

    def deleteOrderByUserEmail(self, email):
        return self.db.delete_many({"uemail": email})

    def countCompleteOrders(self):
        count = self.db.count({"payment_status": 'complete'})
        return count

    def countPendingOrders(self):
        count = self.db.count({"payment_status": 'pending'})
        return count

    def countCanceledOrders(self):
        count = self.db.count({"payment_status": 'canceled'})
        return count

    def countUnshippedOrders(self):
        count = self.db.count({"shipping": 'not_shipped'})
        return count

    def getOrderSequenceNumber(self):
        db = client.AutoAirGroupdb.orders_sequence_number
        collection = db.find_one({"_id": ObjectId('5af085fd5b156909a2160b50')})
        sequence = collection['current_oid']
        return sequence

    def updateOrderSequenceNumber(self, newSequence):
        try:
            db = client.AutoAirGroupdb.orders_sequence_number
            db.update({"_id": ObjectId('5af085fd5b156909a2160b50')}, {'$set': {'current_oid': newSequence}})
            return True
        except:
            return False