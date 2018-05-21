from config.dbconfig import client


class PassResetDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.pass_reset

    def addToResetTable(self, user, auth):
        """
        Adds a user and reset key to database.
        :param user: User email or staff eid.
        :param auth: The generated key.
        :return: Databse insert key.
        """
        key = {
            'user': user,
            'auth': auth
        }
        return self.db.insert_one(key)

    def retrieveFromResetTable(self, auth):
        """
        Recovers the key corresponding to the user from the database.
        Removes the key afterwards.
        :param auth: The users code.
        :return: The entire key for the user.
        """
        key = self.db.find_one({'auth': auth})
        key = key['user']
        self.db.delete_many({'user': key})  #
        return key

    def generateAdminLinkReset(self, id):
        """
        Generates an admin reset link.
        :param id: The id of the admin or staff member.
        :return: The key for the admin or staff.
        """
        key = self.db.find_one({'user': id})
        print("Value of generateAdminLinkReset: " + str(key))
        return key['auth']
