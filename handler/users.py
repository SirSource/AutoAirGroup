from dao.users import UsersDao
from validate_email import validate_email


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
            return False
        else:
            return user

    def getUserByEmail(self, email):
        dao = UsersDao()
        user = dao.getUserByEmail(email)
        if user == None:
            return False
        else:
            return user

    def getUserByPhone(self, phone):
        dao = UsersDao()
        user = dao.getUserByPhone()
        if user == None:
            return False
        else:
            return user

    def insertUser(self, name, last, usertype, email, password, phone, city, place, street, zip):
        if self.userExists(email):
            return False
        else:
            UsersDao().insertUser(name, last, usertype, email, password, phone, city, place, street, zip)
            return True

    def updateUserAddress(self, email, city, place, street, zip):
        if self.userExists(email):
            address = {
                "city": city,
                "place": place,
                "street": street,
                "zipcode": zip
            }
            UsersDao().updateUserAddress(email, address)
        else:
            return False

    def updateUserPhone(self, email, phone):
        if self.validPhone(phone):
            if self.userExists(email):
                UsersDao().updateUserPhone(phone)
                return True
            else:
                return False
        else:
            return False

    def updateUserEmail(self, email, newEmail):
        if self.validEmail(newEmail):
            if self.userExists(email):
                UsersDao().updateUserEmail(email, newEmail)
                return True
            else:
                return False
        else:
            return False

    def updateUserPassword(self, email, password):
        if self.validPassword(password):
            if self.userExists(email):
                UsersDao().updateUserPassword(email, password)
                return True
            else:
                return False
        else:
            return False

    def deleteUserByEmail(self, email):
        if self.userExists(email):
            UsersDao().deleteUserByEmail(email)
            return True
        else:
            return False

    def deleteUserbyPhone(self, phone):
        if self.userExists(phone):
            UsersDao().deleteUserbyPhone(phone)
            return True
        else:
            return False

    def userAuthenticate(self, email, password):
        systemPass = UsersDao().getUserPass(email)
        if systemPass == password:
            return True
        else:
            return False


    # TODO add handler for other functions (getUserByUsername, getUserByEmail, etc.)

    # ---Auxiliary Methods--- #
    def userExists(self, email):
        user = UsersDao().getUserByEmail(email)
        if user == None:
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
