from dao.users import UsersDao
from utilities.valid import Valid as v


class UserHandler:

    def user_dictionary(self, row):
        """
        Creates a user dictionary from database retrieval.
        :param row: Raw user data.
        :return: Formatted user dictionary.
        """
        address = row['user_address']
        del row['user_address']
        del row['_id']
        result = {**address, **row}
        return result

    def getAllUsers(self):
        """
        Fetch all users.
        :return: List of all users.
        """
        dao = UsersDao()
        list = dao.getAllUsers()
        result_list = []
        for row in list:
            result = self.user_dictionary(row)
            result_list.append(result)
        return result_list

    def getUserByUsername(self, username):
        """
        Fetch a user by the username.
        :param username: Username to lookup.
        :return: The user, or False and message.
        """
        dao = UsersDao()
        user = dao.getUserByUsername(username)
        if user == None:
            return False, 'no_user'
        else:
            return user

    def getUserByEmail(self, email):
        """
        Fetch a user by their email address.
        :param email: The email of the user.
        :return: The user or False and message.
        """
        dao = UsersDao()
        user = dao.getUserByEmail(email)
        if user == None:
            return False, 'no_user'
        else:
            return user

    def getUserByEmailReset(self, email):
        """
        Retrieve a user by their email address for resetting password.
        :param email: User email address.
        :return: The user or False and message.
        """
        dao = UsersDao()
        user = dao.getUserByEmail(email)
        if user == None:
            return False, 'no_user'
        else:
            return True, user

    def getUserByPhone(self, phone):
        """
        Fetch user by their phone number.
        :param phone: User phone number.
        :return: The user or False and message.
        """
        dao = UsersDao()
        user = dao.getUserByPhone()
        if user == None:
            return False, 'no_user'
        else:
            return user

    def insertUser(self, form):
        """
        Create a new user from registration form.
        :param form: The user's details from the form.
        :return: Boolean, user email or message if failed.
        """
        # Get form data and validate using utils.validate.
        name = v().removeSpecialChars(form['first_name'])
        last = v().removeSpecialChars(form['last_name'])
        usertype = v().sanitize(form['user'])
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
        """
        Insert a user address or update.
        :param email: Email of the user.
        :param form: Address details from form.
        :return: Boolean and message.
        """
        city = form['city']
        address1 = v().removeSpecialChars(form['address1'])
        address2 = v().removeSpecialChars(form['address2'])
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
        """
        Update the user phone number.
        :param email: User email.
        :param phone: New phone number.
        :return: Boolean, message.
        """
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
        """
        Update the user email address.
        :param email: The current email address.
        :param newEmail: New email address.
        :return: Boolean, message for front end.
        """
        if email == '' or newEmail == '':
            return False, 'invalid_form'
        if v().validEmail(newEmail):
            if self.userExists(email):
                UsersDao().updateUserEmail(email, newEmail)
                return True, 'updated_email'
            else:
                return False, 'no_user'
        else:
            return False, 'invalid_email'

    def updateUserPassword(self, email, form):
        """
        Ùpdate the user's password.
        :param email: Email of the user.
        :param form: Form with user old and new password.
        :return: Boolean and message for front end.
        """
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
        """
        Update user password from password reset.
        :param email: User's email address.
        :param form: Form with old and new password.
        :return: Boolean, message for front end.
        """
        newPassword = form['newPass']
        if newPassword == '':
            return False, 'invalid_form'
        if v().validPassword(newPassword) and self.userExists(email):
            UsersDao().updateUserPassword(email, v().encrypt(newPassword))
            return True, 'updated_password'
        else:
            return False, 'invalid_password'

    def deleteUserByEmail(self, email):
        """
        Remove a user by email address.
        :param email: User email address
        :return: Boolean, message for front end.
        """
        if self.userExists(email):
            UsersDao().deleteUserByEmail(email)
            return True, 'user_deleted'
        else:
            return False, 'delete_error'

    def deleteUserbyPhone(self, phone):
        """
        Delete a user by using their phone number.
        :param phone: The user's phone number.
        :return: Boolean, message for front end.
        """
        if self.userExists(phone):
            UsersDao().deleteUserbyPhone(phone)
            return True, 'user_deleted'
        else:
            return False, 'delete_error'

    def userAuthenticate(self, form):
        """
        Check is user exists and passwords match.
        :param form: Form with user information.
        :return: Boolean, email if any, message for front end.
        """
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
        """
        Validate if user exists in the system database.
        :param email: Email of user to find.
        :return: True if exists, False if not.
        """
        user = UsersDao().getUserByEmail(email)
        if user == None:
            return False
        else:
            return True

    def formToFormattedUser(self, form):
        """
        Create user information from form during an order.
        :param form: Form containing the user information.
        :return: Boolean, user, message for front end.
        """
        # From from validate using utils.validate methods.
        name = v().removeSpecialChars(form['ufirst'])
        last = v().removeSpecialChars(form['ulast'])
        email = v().toLower(form['uemail'])
        phone = form['uphone']
        city = form['city']
        address1 = v().removeSpecialChars(form['address1'])
        address2 = v().removeSpecialChars(form['address2'])
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
