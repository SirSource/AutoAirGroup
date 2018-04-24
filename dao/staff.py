from config.dbconfig import client

class StaffDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.user_admin

    def getAllStaff(self):
        allStaff = []
        staff = self.db
        for doc in staff.find():
            allStaff.append(doc)
        return allStaff

    def getStaffByEid(self, eid):
        staff = self.db.find_one({"eid": eid})
        return staff

    def getStaffByName(self, fname):
        staff = self.db.find({"staff_fname": fname})
        return staff

    def getStaffByLastName(self, lname):
        staff = self.db.find({"staff_lname": lname})
        return staff

    def getStaffByEmail(self, email):
        staff = self.db.find_one({"staff_email": email})
        return staff

    def getStaffPass(self, eid):
        staff = self.getStaffByEid(eid)
        return staff['staff_password']

    def insertStaff(self, name, last, eid, isAdmin, email, password, store):
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
        return self.db.update({'eid': eid}, {'$set':{'admin': admin}})

    def updateStaffStore(self, eid, store):
        return self.db.update({'eid': eid}, {'$set': {'staff_store': store}})

    def updateStaffEmail(self, eid, email):
        return self.db.update({'eid': eid}, {'$set': {'staff_email': email}})

    def updateStaffPassword(self, eid, newPassword):
        return self.db.update({'eid': eid}, {'$set': {'staff_password': newPassword}})

    def deleteStaffByEmail(self, email):
        return self.db.delete_many({"staff_email": email})

    def deleteStaffbyEid(self, eid):
        return self.db.delete_many({"eid": eid})