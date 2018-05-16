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

    def retrieveFromResetTable(self, auth):
        key = self.db.find_one({'auth': auth})
        key = key['user']
        print('user is: ' + str(key))
        self.db.delete_many({'user': key})  #
        return key

    def generateAdminLinkReset(self, auth):
        key = self.db.find_one({'auth': auth})
        key = key['user']
        print('user is: ' + str(key))
        return key