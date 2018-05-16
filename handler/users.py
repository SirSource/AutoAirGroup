from dao.users import UsersDao
from utilities.valid import Valid as v


class UserHandler:

    def user_dictionary(self, row):
        address = row['user_address']
        del row['user_address']
        del row['_id']
        result = {**address, **row}
        return result

    def getAllUsers(self):
        dao = UsersDao()
        list = dao.getAllUsers()
        result_list = []
        for row in list:
            result = self.user_dictionary(row)
            result_list.append(result)
        return result_list

    def getUserByUsername(self, username):
        dao = UsersDao()
        user = dao.getUserByUsername(username)
        if user == None:
            return False, 'no_user'
        else:
            return user

    def getUserByEmail(self, email):
        dao = UsersDao()
        user = dao.getUserByEmail(email)
        if user == None:
            return False, 'no_user'
        else:
            return user

    def getUserByEmailReset(self, email):
        dao = UsersDao()
        user = dao.getUserByEmail(email)
        if user == None:
            return False, 'no_user'
        else:
            return True, user

    def getUserByPhone(self, phone):
        dao = UsersDao()
        user = dao.getUserByPhone()
        if user == None:
            return False, 'no_user'
        else:
            return user

    def insertUser(self, form):
        name = form['first_name']
        last = form['last_name']
        usertype = form['user']
        email = form['email'].lower()
        password = form['password']
        address = {
            "city": "",
            "address1": "",
            "address2": "",
            "zipcode": ""
        }
        if not v().validEmail(email):
            return False, 'invalid_email'
        elif self.userExists(email):
            return False, 'user_exists'
        elif not v().validPassword(password):
            return False, 'invalid_password'
        UsersDao().insertUser(name, last, usertype, email, address, v().encrypt(password))
        return True, email

    def updateUserAddress(self, email, form):
        city = form['city']
        address1 = form['address1']
        address2 = form['address2']
        zip = form['zipcode']

        if email == '' or city == '' or address1 == '' or zip == '':
            return False, 'invalid_form'

        if not v().validZip(zip):
            return False, 'invalid_zip'

        if self.userExists(email):
            address = {
                "city": city,
                "address1": address1,
                "address2": address2,
                "zipcode": zip
            }
            UsersDao().updateUserAddress(email, address)
            return True, 'address_updated'
        else:
            return False, 'address_not_updated'

    def updateUserPhone(self, email, phone):
        if email == '' or phone == '':
            return False, 'invalid_form'
        if v().validPhone(phone):
            if self.userExists(email):
                UsersDao().updateUserPhone(phone)
                return True, 'updated_phone'
            else:
                return False, 'no_user'
        else:
            return False, 'invalid_phone'

    def updateUserEmail(self, email, newEmail):
        if email == '' or newEmail == '':
            return False, 'invalid_form'
        if v().validEmail(newEmail):
            if self.userExists(email):
                UsersDao().updateUserEmail(email, newEmail)
                return True, 'updated_email'
            else:
                return False, 'no_user'
        else:
            return False
            'invalid_email'

    def updateUserPassword(self, email, form):
        password = form['current_pass']
        newPassword = form['new_pass']
        if email == '' or password == '' or newPassword == '':
            return False, 'invalid_form'
        if v().validPassword(newPassword) and self.userExists(email):
            bool = self.userAuthenticate(form={'email': email, 'password': password})[0]
            if bool:
                UsersDao().updateUserPassword(email, v().encrypt(newPassword))
                return True, 'updated_password'
            else:
                return False, 'invalid_old_password'
        else:
            return False, 'invalid_password'

    def updateUserPasswordReset(self, email, form):
        newPassword = form['newPass']
        if newPassword == '':
            return False, 'invalid_form'
        if v().validPassword(newPassword) and self.userExists(email):
            UsersDao().updateUserPassword(email, v().encrypt(newPassword))
            return True, 'updated_password'
        else:
            return False, 'invalid_password'

    def deleteUserByEmail(self, email):
        if self.userExists(email):
            UsersDao().deleteUserByEmail(email)
            return True, 'user_deleted'
        else:
            return False, 'delete_error'

    def deleteUserbyPhone(self, phone):
        if self.userExists(phone):
            UsersDao().deleteUserbyPhone(phone)
            return True, 'user_deleted'
        else:
            return False, 'delete_error'

    def userAuthenticate(self, form):
        email = form['email'].lower()
        password = form['password']
        systemPass = UsersDao().getUserPass(email)
        try:
            if v().decrypt(password, systemPass):
                return True, email, 'login_success'
            else:
                return False, None, 'login_fail'
        except:
            return False, None, 'login_fail'

    # ---Auxiliary Methods--- #
    def userExists(self, email):
        user = UsersDao().getUserByEmail(email)
        if user == None:
            return False
        else:
            return True

    def formToFormattedUser(self, form):
        name = form['ufirst']
        last = form['ulast']
        email = form['uemail']
        phone = form['uphone']
        city = form['city']
        address1 = form['address1']
        address2 = form['address2']
        zipcode = form['zipcode']

        if name == '' or last == '' or email == '' or phone == '' or city == '' or address1 == '' or zipcode == '':
            return False, None, 'invalid_form'

        if not v().validZip(zipcode):
            return False, None, 'invalid_zip'

        if not v().validPhone(phone):
            return False, None, 'invalid_phone'

        if not v().validEmail(email):
            return False, None, 'invalid_email'

        user = {
            'ufirst': name,
            'ulast': last,
            'uemail': email,
            'uphone': phone,
            'city': city,
            'address1': address1,
            'address2': address2,
            'zipcode': zipcode
        }

        return True, user, 'user_formatted'
