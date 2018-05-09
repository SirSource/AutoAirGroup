from config.dbconfig import client


class UsersDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.user_account

    def getAllUsers(self):
        """
        Fetch all the users from the database.
        :return: A list of all users in the database.
        """
        allUsers = []
        users = self.db
        for doc in users.find():
            allUsers.append(doc)
        return allUsers

    def getUserByUsername(self, username):
        """
        Fetch a user by a specified username.
        :param username: The username of the user to be fetched.
        :return: The user information that matches the username provided.
        """
        user = self.db.find_one({"username": username})
        return user

    def getUserByEmail(self, email):
        """
        Fetch a user by a specified email.
        :param email: The email of the user to be fetched.
        :return: The user information that matches the email provided.
        """
        user = self.db.find_one({"user_email": email})
        return user

    def getUserByPhone(self, phone):
        """
        Fetch a user by a specified phone number.
        :param phone: The phone of the user to be fetched.
        :return: The user information that matches the phone provided.
        """
        user = self.db.find_one({"user_phone": phone})
        return user

    def insertUser(self, name, last, usertype, email, address, password):
        """
        Insert a new user into the database.
        :param name: First name
        :param last: Last name
        :param usertype: Type of user
        :param email: Email for user
        :param password: Password for user
        :param phone: Phone for user
        :param city: City for user
        :param place: Place of residence for user
        :param street: Street for user
        :param zip: Zip for user
        :return: User ID
        """
        newUser = {
            "user_fname": name,
            "user_lname": last,
            "usertype": usertype,
            "user_email": email,
            "user_address": address,
            "user_password": password,
        }
        return self.db.insert_one(newUser).inserted_id

    def updateUserAddress(self, email, address):
        """
        Updates the address of the user in the system.
        :param email: Email of the user to update.
        :param address: The new address dictionary for the user.
        :return: Mongodb ObjectID.
        """
        return self.db.update({'user_email': email}, {'$set': {'user_address': address}})

    def updateUserPhone(self, email, phone):
        """
        Updates the phone number of the user.
        :param email: Email of the user to update.
        :param phone: New phone number for the user.
        :return: Mongodb ObjectID.
        """
        return self.db.update({'user_email': email}, {'$set': {'user_phone': phone}})

    def updateUserEmail(self, email, newEmail):
        """
        Updates the email address number of the user.
        :param email: Email of the user to update.
        :param newEmail: New email for the user.
        :return: Mongodb ObjectID.
        """
        return self.db.update({'user_email': email}, {'$set': {'user_email': newEmail}})

    def updateUserPassword(self, email, password):
        """
        Updates the password of the user.
        :param email: Email of the user to update.
        :param password: The new password for the user.
        :return: Mongodb ObjectID.
        """
        return self.db.update({'user_email': email}, {'$set': {'user_password': password}})

    def getUserPass(self, email):
        """
        Retrieve the password for the user.
        :param email: Email of the user.
        :return: The user's password.
        """
        user = self.getUserByEmail(email)
        if user == None:
            return None
        return user['user_password']

    def deleteUserByEmail(self, email):
        """
        Delete a user by the provided email
        :param email: User email
        :return: MongoDB delete ID
        """
        return self.db.delete_many({"user_email": email})

    def deleteUserbyPhone(self, phone):
        """
        Delete a user by the provided phone
        :param phone: User phone number
        :return: MongoDB delete ID
        """
        return self.db.delete_many({"user_phone": phone})
