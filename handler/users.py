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
        if v().validPhone(phone):
            if self.userExists(email):
                UsersDao().updateUserPhone(phone)
                return True
            else:
                return False
        else:
            return False

    def updateUserEmail(self, email, newEmail):
        if v().validEmail(newEmail):
            if self.userExists(email):
                UsersDao().updateUserEmail(email, newEmail)
                return True
            else:
                return False
        else:
            return False

    def updateUserPassword(self, email, password, newPassword):
        if v().validPassword(newPassword) and self.userExists(email):
            if self.userAuthenticate(email, password):
                UsersDao().updateUserPassword(email, newPassword)
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
