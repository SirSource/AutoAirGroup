from config.dbconfig import client
import json


class UsersDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.user_account

    def getAllUsers(self):
        users = self.db
        for doc in users.find():
            print(doc)
        print("test")

    def insertUser(self):
        address = {
            "city": "Rincon",
            "place": "Urb Esteves",
            "street": "Calle Cipreses",
            "zipcode": "00676"
        }

        newUser = {
            "user_fname": "Juan",
            "user_lname:": "DelPueblo",
            "username:": "jdp",
            "usertype:": "customer",
            "user_email": "jdp@gmail.com",
            "user_password": "jdp123",
            "user_address": address,
            "user_phone": 7871234567
        }
        self.db.insert_one(newUser).inserted_id