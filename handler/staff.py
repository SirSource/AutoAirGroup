from dao.staff import StaffDao


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

    # --Auxilliary Functions-- #
    def stringToBool(self, string):
        if string == 'True':
            return True
        else:
            return False

    def staffExists(self, eid, email):
        dao = StaffDao()
        staff = dao.getStaffByEid(eid)
        staffEmail = dao.getStaffByEmail(email)
        if staff == None and staffEmail == None:
            return False
        else:
            return True

# TODO add handler for other functions (getUserByUsername, getUserByEmail, etc.)
