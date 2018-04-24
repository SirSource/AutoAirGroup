from dao.staff import StaffDao
from validate_email import validate_email


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
        if self.staffExists(eid) and self.validEmail(email):
            StaffDao().updateStaffEmail(eid, email)
            return True
        else:
            return False

    def updateStaffPassword(self, eid, password, newPassword):
        if self.validPassword(newPassword) and self.staffExists():
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
        if fname == '' or lname == '' or eid == '' or email == '' or store == '' or admin == '':
            return False
        elif self.staffExists(eid, email):
            return False
        else:
            StaffDao().insertStaff(fname, lname, eid, admin, email, "temporary", store)
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

    def validPhone(self, phone):
        if not phone.isdigit() or len(phone) < 10:
            return False
        else:
            return True

    def validEmail(self, email):
        is_valid = validate_email(email)
        if is_valid:
            return True
        else:
            return False

    def validPassword(self, password):
        symbol = ['$', '@', '#']
        if len(password) < 6:
            return False
        if len(password) > 15:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char in symbol for char in password):
            return False
        return True

    def staffAuthenticate(self, eid, password):
        systemPass = StaffDao().getStaffPass(eid)
        if systemPass == password:
            return True
        else:
            return False
# TODO add handler for other functions (getUserByUsername, getUserByEmail, etc.)
