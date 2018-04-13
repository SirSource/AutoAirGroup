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
        print("The list of users includes:\n")
        return allUsers

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

    def insertUser(self, name, last, user, usertype, email, password, phone, city, place, street, zip):
        """
        Insert a new user into the database.
        :param name: First name
        :param last: Last name
        :param user: Username
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
        #User address dictionary
        address = {
            "city": city,
            "place": place,
            "street": street,
            "zipcode": zip
        }
        #New user dictionary
        newUser = {
            "user_fname": name,
            "user_lname:": last,
            "username:": user,
            "usertype:": usertype,
            "user_email": email,
            "user_password": password,
            "user_address": address,
            "user_phone": phone
        }
        return self.db.insert_one(newUser).inserted_id

    def updateUserAddress(self, username, city, place, street, zip):
        # TODO: implement
        # Must be able to change the address of the user
        # who's username is provided as a parameter
        # return user ID
        # Document the function
        address = {
            "city": city,
            "place": place,
            "street": street,
            "zipcode": zip
        }
        return None

    def updateUserPhone(self, username, phone):
        # TODO: implement
        # Update the phone number of the user who's
        # username is provided
        # Document the function
        return None

    def updateUserEmail(self, username, email):
        # TODO: implement
        # Update the email of the user who's
        # username is provided
        # Document the function
        return None

    def updateUserPassword(self, username, password):
        # TODO: implement
        # Update the password of the user who's
        # username is provided
        # Document the function
        return None

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