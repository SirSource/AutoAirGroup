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

    def getStaffByEid(self, form):
        eid = v().toLower(form['eid'])
        if eid == '':
            return False, None, 'invalid_eid'
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False, None, 'no_staff'
        else:
            return True, staff, 'staff_exists'

    def getStaffByEidMain(self, eid):
        if eid == '':
            return False, None, 'invalid_eid'
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False, None, 'no_staff'
        else:
            return True, staff, 'staff_exists'

    def getStaffByEmail(self, email):
        if email == '':
            return False, None, 'invalid_email'
        dao = StaffDao()
        staff = dao.getStaffByEmail(email)
        if staff == None:
            return False, None, 'no_staff'
        else:
            return True, staff, 'staff_exists'

    def updateStaffAsAdmin(self, eid, form):
        admin = form['admin']
        if eid == '' or admin == '':
            return False, 'invalid_form'
        if self.staffExists(eid):
            dao = StaffDao()
            dao.updateStaffAsAdmin(eid, v().stringToBool(admin))
            return True, 'updated_admin'
        else:
            return False, 'no_staff'

    def updateStaffStore(self, eid, form):
        store = form['store']
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
            bool = self.staffAuthenticateChange(eid, password)[0]
            if bool:
                StaffDao().updateStaffPassword(eid, v().encrypt(newPassword))
                return True, 'updated_password'
            else:
                return False, 'invalid_password'
        else:
            return False, 'invalid_new_password'

    def insertStaff(self, form):
        fname = form['first_name']
        lname = form['last_name']
        eid = v().toLower(form['eid'])
        email = v().toLower(form['email'])
        store = form['store']
        admin = v().stringToBool(form['admin'])
        password = self.generatePassword()
        if fname == '' or lname == '' or eid == '' or email == '' or store == '' or admin == '':
            return False, 'invalid_form'
        elif self.staffExists(eid):
            return False, 'staff_exists'
        else:
            StaffDao().insertStaff(fname, lname, eid, admin, email, v().encrypt(password), store)
            return True, 'staff_created'

    def deleteStaff(self, form):
        eid = v().toLower(form['eid'])
        if eid == '':
            return False, 'invalid_form'
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

    def staffAuthenticateChange(self, eid, password):
        if eid == '' or password == '':
            return False, None, 'invalid_form'
        systemPass = StaffDao().getStaffPass(eid)
        if v().decrypt(password, systemPass):
            return True, eid, 'staff_auth'
        else:
            return False, None, 'staff_auth_failed'

    def staffAuthenticate(self, form):
        eid = form['eid'].lower()
        password = form['password']
        if eid == '' or password == '':
            return False, None, 'invalid_form'
        systemPass = StaffDao().getStaffPass(eid)
        if v().decrypt(password, systemPass):
            return True, eid, 'staff_auth'
        else:
            return False, None, 'staff_auth_failed'

    def generatePassword(self):
        minlength = 8
        maxlength = 12
        chars = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return password

    def staffIsAdmin(self, eid):
        admin = StaffDao().staffIsAdmin(eid)
        if admin == None:
            return False, 'no_staff'
        elif admin == True:
            return True, 'is_admin'
        else:
            return False, 'not_admin'
