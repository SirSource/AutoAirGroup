from config.dbconfig import client
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128


class OrdersDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.orders

    def getAllOrders(self):
        """
        Retrieve all orders from the database.
        :return: a list of all orders
        """
        allOrders = []
        orders = self.db
        for doc in orders.find():
            allOrders.append(doc)
        return allOrders

    def getOrdersByOrderID(self, oid):
        """
        Retrieve orders with a specific order id.
        :param oid: The id for the order to retrieve
        :return: the order that matches the id.
        """
        order = self.db.find_one({"orderid": int(oid)})
        return order

    def getOrdersByEmail(self, email):
        """
        Retrieve all orders that match a customer's email address
        :param email: The email of the customer to search for.
        :return: All orders from the customer with matching email.
        """
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"uemail": email}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def getOrdersByPhone(self, phone):
        """
        Retrieve all orders by matching phone numbers.
        :param phone: The phone number of the customer.
        :return: All orders that have the same matching phone number
        """
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"uphone": phone}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def getOrdersByStatus(self, status):
        """
        Retrieve all orders that match a given status.
        :param status: The current status of the order.
        :return: A list of all orders that match that status.
        """
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"payment_status": status}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def getOrdersShipped(self):
        """
        Retrieve all orders that have shipped.
        :return: All orders that have a shipping status og 'shipped'
        """
        allOrders = None
        tempList = []
        orders = self.db
        for doc in orders.find({"shipping": "shipped"}):
            tempList.append(doc)
        if len(tempList) > 0:
            allOrders = tempList
        return allOrders

    def insertOrder(self, orderid, user, total, ivu, taxed,
                    grandTotal, shipping, date, products):
        """
        :param orderid:
        :param ufirst:
        :param ulast:
        :param city:
        :param place:
        :param street:
        :param zipcode:
        :param uemail:
        :param uphone:
        :param total:
        :param ivu:
        :param payment_status:
        :param shipping:
        :param date:
        :param products:
        :return:
        """
        address = {
            "city": user['city'],
            "address1": user['address1'],
            "address2": user['address2'],
            "zipcode": user['zipcode']
        }
        order = {
            'orderid': orderid,
            'ufirst': user['ufirst'],
            'ulast': user['ulast'],
            'uemail': user['uemail'],
            'uphone': user['uphone'],
            'address': address,
            'total': total,
            'ivu': ivu,
            'tax_total': taxed,
            'shipping_total': shipping,
            'grand_total': grandTotal,
            'payment_status': 'pending',
            'shipping': 'not_shipped',
            'date': date,
            'products': products
        }
        self.db.insert_one(order).inserted_id
        return True, orderid

    def updateOrderStatusForm(self, oid, status):
        """
        Finds a specific order and updates its status.
        :param oid: The id of the order to update.
        :param status: The new status (provided from the form, passed to the handler.)
        :return: Database objectid.
        """
        return self.db.update({'orderid': int(oid)}, {'$set': {'payment_status': status}})

    def updateOrderShippingForm(self, oid, status):
        """
        Finds a specific order and updates its shipping status.
        :param oid: The id of the order to update.
        :param status: The new shipping status (provided from the form, passed to the handler.)
        :return: Database objectid.
        """
        return self.db.update({'orderid': int(oid)}, {'$set': {'shipping': status}})

    def deleteOrderById(self, oid):
        """
        Remove an order from the database using the ID.
        :param oid: The ID of the order to remove.
        :return: Database objectid.
        """
        return self.db.delete_many({"orderid": int(oid)})

    def deleteOrderByUserEmail(self, email):
        """
        Remove an order from the database using the ID.
        :param email: The email of the order to remove.
        :return: Database objectid.
        """
        return self.db.delete_many({"uemail": email})

    def countCompleteOrders(self):
        """
        Returns the number of orders that are complete.
        :return: An integer representing the number of complete orders.
        """
        count = self.db.count({"payment_status": 'complete'})
        return count

    def countPendingOrders(self):
        """
        Returns the number of orders that are pending.
        :return: An integer representing the number of pending orders.
        """
        count = self.db.count({"payment_status": 'pending'})
        return count

    def countCanceledOrders(self):
        """
        Returns the number of orders that are canceled.
        :return: An integer representing the number of canceled orders.
        """
        count = self.db.count({"payment_status": 'canceled'})
        return count

    def countUnshippedOrders(self):
        """
        Returns the number of orders that are not shipped yet.
        :return: An integer representing the number of unshipped orders.
        """
        count = self.db.count({"shipping": 'not_shipped'})
        return count

    def getOrderSequenceNumber(self):
        """
        Retrieved from the database the last order number used in order to continue the sequence.
        :return: The last order number used.
        """
        db = client.AutoAirGroupdb.orders_sequence_number
        collection = db.find_one({"_id": ObjectId('5af085fd5b156909a2160b50')})
        sequence = collection['current_oid']
        return sequence

    def updateOrderSequenceNumber(self, newSequence):
        """
        Updates the last order number used.
        :param newSequence: The newly generated order number.
        :return: True if operation successful, False otherwise.
        """
        try:
            db = client.AutoAirGroupdb.orders_sequence_number
            db.update({"_id": ObjectId('5af085fd5b156909a2160b50')}, {'$set': {'current_oid': newSequence}})
            return True
        except:
            return False
