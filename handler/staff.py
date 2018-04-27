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
        if eid == '':
            return False, 'invalid_eid'
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False, 'no_staff'
        else:
            return staff, 'staff_exists'

    def getStaffByEmail(self, email):
        if email == '':
            return False, 'invalid_email'
        dao = StaffDao()
        staff = dao.getStaffByEmail(email)
        if staff == None:
            return False, 'no_staff'
        else:
            return staff, 'staff_exists'

    def updateStaffAsAdmin(self, eid, admin):
        if eid == '' or admin == '':
            return False, 'invalid_form'
        if self.staffExists(eid):
            dao = StaffDao()
            dao.updateStaffAsAdmin(eid, admin)
            return True, 'updated_admin'
        else:
            return False, 'no_staff'

    def updateStaffStore(self, eid, store):
        if eid == '' or store == '':
            return False, 'invalid_form'
        if self.staffExists(eid):
            dao = StaffDao()
            dao.updateStaffStore(eid, store)
            return True, 'updated_store'
        else:
            return False, 'no_staff'

    def updateStaffEmail(self, eid, email):
        if eid == '' or email == '':
            return False, 'invalid_form'
        if self.staffExists(eid) and v().validEmail(email):
            StaffDao().updateStaffEmail(eid, email)
            return True, 'updated_email'
        else:
            return False, 'no_staff'

    def updateStaffPassword(self, eid, password, newPassword):
        if password == '' or newPassword == '':
            return False, 'invalid_form'
        if v().validPassword(newPassword) and self.staffExists(eid):
            if self.staffAuthenticate(eid, password):
                StaffDao().updateStaffPassword(eid, newPassword)
                return True, 'updated_password'
            else:
                return False, 'invalid_password'
        else:
            return False, 'invalid_password'

    def insertStaff(self, form):
        fname = form['first_name']
        lname = form['last_name']
        eid = form['eid']
        email = form['email']
        store = form['store']
        admin = v().stringToBool(form['admin'])
        password = self.generatePassword()
        if fname == '' or lname == '' or eid == '' or email == '' or store == '' or admin == '':
            return False, 'invalid_form'
        elif self.staffExists(eid):
            return False, 'staff_exists'
        else:
            StaffDao().insertStaff(fname, lname, eid, admin, email, password, store)
            return True, 'staff_created'

    def deleteStaff(self, eid):
        if self.staffExists(eid):
            StaffDao().deleteStaffbyEid(eid)
            return True, 'staff_deleted'
        else:
            return False, 'delete_error'

    # --Auxilliary Functions-- #

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
