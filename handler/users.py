from dao.users import UsersDao


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

    def insertUser(self, name, last, usertype, email, password, phone, city, place, street, zip):
        if self.userExists(email):
            return False
        else:
            UsersDao().insertUser(name, last, usertype, email, password, phone, city, place, street, zip)
            return True



    # TODO add handler for other functions (getUserByUsername, getUserByEmail, etc.)

    # ---Auxiliary Methods--- #
    def userExists(self, email):
        user = UsersDao().getUserByEmail(email)
        if user == None:
            return False
        else:
            return True