from dao.staff import StaffDao
from dao.passReset import PassResetDao as passDao
import string
from random import *
from utilities.valid import Valid as v
from dao.passReset import PassResetDao as pr
from utilities.sendmail import SendMail as mail


class StaffHandler:

    def user_dictionary(self, row):
        """
        Creates a dictionary for returning staff information.
        :param row: Staff raw data
        :return: Formatted list without ID
        """
        del row['_id']
        return row

    def getAllStaff(self):
        """
        Fetch all staff from the database.
        :return: List of all staff members.
        """
        dao = StaffDao()
        list = dao.getAllStaff()
        result_list = []
        for row in list:
            result = self.user_dictionary(row)
            result_list.append(result)
        return result_list

    def getStaffByEid(self, form):
        """
        Fetch a staff member by the id form.
        :param form: A form from the main method including the id.
        :return: Boolean, staff (if exists), message for front end.
        """
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
        """
        Fetch a staff member by the id directly.
        :param eid: Id of staff member.
        :return: Boolean, staff (if exists), message for front end.
        """
        if eid == '':
            return False, None, 'invalid_eid'
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False, None, 'no_staff'
        else:
            return True, staff, 'staff_exists'

    def getStaffByEmail(self, email):
        """
        Fetch staff by email.
        :param email: Email of staff member.
        :return: Boolean, staff (if exists), message for front end.
        """
        if email == '':
            return False, None, 'invalid_email'
        dao = StaffDao()
        staff = dao.getStaffByEmail(email)
        if staff == None:
            return False, None, 'no_staff'
        else:
            return True, staff, 'staff_exists'

    def updateStaffAsAdmin(self, eid, form):
        """
        Update the status of the staff member.
        :param eid: Id of staff member.
        :param form: Values submitted through a form.
        :return: Boolean, message for front end.
        """
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
        """
        Update the staff member store.
        :param eid: Id of staff.
        :param form: Form with the status to change to.
        :return: Boolean, message for front end.
        """
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
        """
        Update the staff email address.
        :param eid: Id of staff member.
        :param email: New email of staff member.
        :return: Boolean, message for front end.
        """
        if eid == '' or email == '':
            return False, 'invalid_form'
        if self.staffExists(eid) and v().validEmail(email):
            StaffDao().updateStaffEmail(eid, email)
            return True, 'updated_email'
        else:
            return False, 'no_staff'

    def updateStaffPassword(self, eid, password, newPassword):
        """
        Update the staff password.
        :param eid: Id of staff member.
        :param password: Current password.
        :param newPassword: New Password.
        :return: Boolean, message for front end.
        """
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

    def updateStaffPasswordReset(self, eid, form):
        """
        Update staff password from form.
        :param eid: Id of staff.
        :param form: Form with new values and current password.
        :return: Boolean, smessage for front end.
        """
        newPassword = form['newPass']
        if newPassword == '':
            return False, 'invalid_form'
        if v().validPassword(newPassword) and self.staffExists(eid):
            StaffDao().updateStaffPassword(eid, v().encrypt(newPassword))
            return True, 'updated_password'
        else:
            return False, 'invalid_password'

    def insertStaff(self, form):
        """
        Create a new staff from a form input.
        :param form: Form with staff details to create.
        :return: Boolean, message for front end.
        """
        # extract information from the form and perform validations using utils.validdate.
        fname = v().removeSpecialChars(form['first_name'])
        lname = v().removeSpecialChars(form['last_name'])
        eid = v().toLower(v().sanitize(form['eid']))
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

            # Trigger el handler

            dao = pr()
            dao.addToResetTable(eid, v().generateRandomString())
            key = dao.generateAdminLinkReset(eid)

            # Crear el link
            # link = "http://localhost:5000/user/reset/password/" + str(key)

            # link : localhost:5000/user/reset/password/KEY
            # Envio el email

            m = mail()
            m.sendAccountRecoverEmail(email, key)
            # m.sendChangePasswordLink(email, link)

            return True, 'staff_created'

    def deleteStaff(self, form):
        """
        REmoves staff from database.
        :param form: Staff Id from form.
        :return: Boolean, message for front end.
        """
        eid = v().toLower(form['eid'])
        if eid == '':
            return False, 'invalid_form'
        if eid == 'aag1':
            return False, 'delete_error_super'
        if self.staffExists(eid):
            StaffDao().deleteStaffbyEid(eid)
            return True, 'staff_deleted'
        else:
            return False, 'delete_error'

    # --Auxilliary Functions-- #

    def staffExists(self, eid):
        """
        Verify if staff exists.
        :param eid: Id of staff.
        :return: True if exists, False if not.
        """
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        if staff == None:
            return False
        else:
            return True

    def staffAuthenticateChange(self, eid, password):
        """
        Staff authenticate
        :param eid: Id of staff.
        :param password: Password of staff.
        :return: Boolean, staff id (if exists), message for front end.
        """
        try:
            if eid == '' or password == '':
                return False, None, 'invalid_form'
            systemPass = StaffDao().getStaffPass(eid)
            if not systemPass:
                return False, None, 'staff_auth_failed'
            if v().decrypt(password, systemPass):
                return True, eid, 'staff_auth'
            else:
                return False, None, 'staff_auth_failed'
        except:
            return False, None, 'staff_auth_failed'

    def staffAuthenticate(self, form):
        """
        Staff authenticate from form.
        :param form: Form with staff details.
        :return: Boolean, staff id (if exists), message for front end.
        """
        eid = form['eid'].lower()
        password = form['password']
        if eid == '' or password == '':
            return False, None, 'invalid_form'
        systemPass = StaffDao().getStaffPass(eid)
        try:
            if v().decrypt(password, systemPass):
                return True, eid, 'staff_auth'
            else:
                return False, None, 'staff_auth_failed'
        except:
            return False, None, 'staff_auth_failed'

    def generatePassword(self):
        """
        Generates a random password for new staff member.
        :return: New password string.
        """
        minlength = 8
        maxlength = 12
        chars = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return password

    def staffIsAdmin(self, eid):
        """
        Validate if a staff member is admin or not.
        :param eid: Id of staff member.
        :return: Boolean, message for front end.
        """
        admin = StaffDao().staffIsAdmin(eid)
        if admin == None:
            return False, 'no_staff'
        elif admin == True:
            return True, 'is_admin'
        else:
            return False, 'not_admin'

    def genericStaffSearch(self, string):
        """
        Search for staff id, email, name, last name, workplace.
        :param string: Query
        :return: Staff results.
        """
        string = v().removeSpecialChars(string)
        return StaffDao().genericStaffSearch(string)

    def getResetFromAdmin(self, id):
        """
        Creates areset link form staff member that was just created.
        :param id: Id of staff
        :return: Staff member, message for front end.
        """
        user = pr().generateAdminLinkReset(id)  # user devuelve lo que va a ser el link
        staffHandler = self.getStaffByEidMain(user)
        if staffHandler[0] == False:
            print('no staff')
        else:
            return user, 'staff'
