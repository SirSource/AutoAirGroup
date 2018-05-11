from config.dbconfig import client


class StaffDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.user_admin

    def getAllStaff(self):
        """
        Retrieves all the staff in the system.
        :return: A list of staff.
        """
        allStaff = []
        staff = self.db
        for doc in staff.find():
            allStaff.append(doc)
        return allStaff

    def getStaffByEid(self, eid):
        """
        Retrieves staff members by their ID
        :param eid: The staff's identification number or string.
        :return: The staff member if found, otherwise, None
        """
        staff = self.db.find_one({"eid": eid})
        return staff

    def getStaffByName(self, fname):
        """
        Retrieves staff members by their first name
        :param fname: First name
        :return: The staff member if found, otherwise, None
        """
        staff = self.db.find({"staff_fname": fname})
        return staff

    def getStaffByLastName(self, lname):
        """
        Retrieves staff members by their last name
        :param lname: Last name
        :return: The staff member if found, otherwise, None
        """
        staff = self.db.find({"staff_lname": lname})
        return staff

    def getStaffByEmail(self, email):
        """
        Retrieves staff members by their email
        :param email: email address
        :return: The staff member if found, otherwise, None
        """
        staff = self.db.find_one({"staff_email": email})
        return staff

    def getStaffPass(self, eid):
        """
        Retrieves the password of the staff member.
        :param eid: The id of the staff member
        :return: The password of the staff member.
        """
        staff = self.getStaffByEid(eid)
        return staff['staff_password']

    def staffIsAdmin(self, eid):
        """
        Retrieves the role of the staff member.
        :param eid: The id of the staff member to query.
        :return: True if the staff member is an admin, False otherwise.
        """
        staff = self.getStaffByEid(eid)
        admin = staff['admin']
        return admin

    def insertStaff(self, name, last, eid, isAdmin, email, password, store):
        """
        Insert a staff member into the database.
        :param name: First name of the staff member.
        :param last: Last name of the staff member.
        :param eid: The id of the staff member.
        :param isAdmin: A boolean of True for admin or False if not.
        :param email: Email address of staff member.
        :param password: Password of the staff member.
        :param store: The store of the staff member.
        :return: Returns the ID of the staff member inserted.
        """
        newStaff = {
            "staff_fname": name,
            "staff_lname": last,
            "eid": eid,
            "admin": isAdmin,
            "staff_email": email,
            "staff_password": password,
            "staff_store": store
        }
        return self.db.insert_one(newStaff).inserted_id

    def updateStaffAsAdmin(self, eid, admin):
        """
        Changes the role of the admin.
        :param eid: Id of the staff member.
        :param admin: True for admin, False for regular staff status.
        :return: Object ID of record from mongodb.
        """
        return self.db.update({'eid': eid}, {'$set': {'admin': admin}})

    def updateStaffStore(self, eid, store):
        """
        Changes the store of the staff member.
        :param eid: Id of the staff member.
        :param store: Store to change the staf member to.
        :return: Object ID of record from mongodb.
        """
        return self.db.update({'eid': eid}, {'$set': {'staff_store': store}})

    def updateStaffEmail(self, eid, email):
        """
        Changes the email of the staff member.
        :param eid: Id of the staff member.
        :param email: The new email address for the staff member.
        :return: Object ID of record from mongodb.
        """
        return self.db.update({'eid': eid}, {'$set': {'staff_email': email}})

    def updateStaffPassword(self, eid, newPassword):
        """
        Changes the password of the staff member.
        :param eid: Id of the staff member.
        :param newPassword: New password for the staff member.
        :return: Object ID of record from mongodb.
        """
        return self.db.update({'eid': eid}, {'$set': {'staff_password': newPassword}})

    def deleteStaffByEmail(self, email):
        """
        Deletes a staff member from the database by their email address.
        :param email: Email address of the staff member to delete.
        :return: Object ID of record from mongodb.
        """
        return self.db.delete_many({"staff_email": email})

    def deleteStaffbyEid(self, eid):
        """
        Deletes a staff member from the database by their email address.
        :param eid: Id of the staff member.
        :return: Object ID of record from mongodb.
        """
        return self.db.delete_many({"eid": eid})

    def genericStaffSearch(self, string):
        collection = self.db
        collection.create_index(
            [('staff_fname', 'text'), ('staff_lname', 'text'), ('staff_email', 'text'), ('eid', 'text'), ('staff_store', 'text')])
        find = collection.find({"$text": {"$search": string}}, {"_id": 0})
        staff = []
        for doc in find:
            staff.append(doc)
        return staff
