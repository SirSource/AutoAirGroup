from config.dbconfig import client


class PassResetDao:

    def __init__(self):
        self.db = client.AutoAirGroupdb.pass_reset

    def addToResetTable(self, user, auth):
        key = {
            'user': user,
            'auth': auth
        }
        return self.db.insert_one(key)

    def retrieveFromResetTable(self, user):
        key = self.db.find_one({"user": user})
        key = key['user']
        print('user is: ' + str(key))
        self.db.delete_many({"user": user})
        return key
