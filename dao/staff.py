from config.dbconfig import client

class StaffDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.user_admin

    def getAllStaff(self):
        """
        Fetch all the users from the database.
        :return: A list of all users in the database.
        """
        allStaff = []
        staff = self.db
        for doc in staff.find():
            allStaff.append(doc)
        return allStaff

    def getStaffByEid(self, eid):
        """
        Fetch a user by a specified username.
        :param username: The username of the user to be fetched.
        :return: The user information that matches the username provided.
        """
        staff = self.db.find_one({"username": eid})
        return staff

    def getStaffByEmail(self, email):
        """
        Fetch a user by a specified email.
        :param email: The email of the user to be fetched.
        :return: The user information that matches the email provided.
        """
        staff = self.db.find_one({"user_email": email})
        return staff

    def insertStaff(self, name, last, user, isAdmin, email, password, store):

        #New staff dictionary
        newStaff = {
            "staff_fname": name,
            "staff_lname:": last,
            "eid": user,
            "admin": isAdmin,
            "staff_email": email,
            "staff_password": password,
            "staff_store": store
        }
        return self.db.insert_one(newStaff).inserted_id

    def updateUserAsAdmin(self, admin):
        # TODO: implement
        # Must be able to change the address of the user
        # who's username is provided as a parameter
        # return user ID
        # Document the function
        return self.db.update({'admin': self.getTax()['fee']}, {'$set':{'fee': admin}})

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