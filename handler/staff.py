from dao.staff import StaffDao
import string
from random import *
from utilities.valid import Valid as v


class StaffHandler:

    def user_dictionary(self, row):
        del row['_id']
        return row

    def getAllStaff(self):
        dao = StaffDao()
        list = dao.getAllStaff()
        result_list = []
        for row in list:
            result = self.user_dictionary(row)
            result_list.append(result)
        return result_list

    def getStaffByEid(self, eid):
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False
        else:
            return staff

    def getStaffByEmail(self, email):
        dao = StaffDao()
        staff = dao.getStaffByEmail(email)
        if staff == None:
            return False
        else:
            return staff

    def updateStaffAsAdmin(self, eid, admin):
        if self.staffExists(eid):
            dao = StaffDao()
            dao.updateStaffAsAdmin(eid, admin)
            return True
        else:
            return False

    def updateStaffStore(self, eid, store):
        if self.staffExists(eid):
            dao = StaffDao()
            dao.updateStaffStore(eid, store)
            return True
        else:
            return False

    def updateStaffEmail(self, eid, email):
        if self.staffExists(eid) and v().validEmail(email):
            StaffDao().updateStaffEmail(eid, email)
            return True
        else:
            return False

    def updateStaffPassword(self, eid, password, newPassword):
        if v().validPassword(newPassword) and self.staffExists(eid):
            if self.staffAuthenticate(eid, password):
                StaffDao().updateStaffPassword(eid, newPassword)
                return True
            else:
                return False
        else:
            return False

    def insertStaff(self, form):
        fname = form['first_name']
        lname = form['last_name']
        eid = form['eid']
        email = form['email']
        store = form['store']
        admin = self.stringToBool(form['admin'])
        password = self.generatePassword()
        if fname == '' or lname == '' or eid == '' or email == '' or store == '' or admin == '':
            return False
        elif self.staffExists(eid):
            return False
        else:
            StaffDao().insertStaff(fname, lname, eid, admin, email, password, store)
            return True

    def deleteStaff(self, eid):
        if self.staffExists(eid):
            StaffDao().deleteStaffbyEid(eid)
            return True
        else:
            return False

    # --Auxilliary Functions-- #
    def stringToBool(self, string):
        if string == 'True':
            return True
        else:
            return False

    def staffExists(self, eid):
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False
        else:
            return True

    def staffAuthenticate(self, eid, password):
        systemPass = StaffDao().getStaffPass(eid)
        if systemPass == password:
            return True
        else:
            return False

    def generatePassword(self):
        minlength = 8
        maxlength = 12
        chars = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return password
# TODO add handler for other functions (getUserByUsername, getUserByEmail, etc.)
