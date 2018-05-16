from dao.passReset import PassResetDao as pr
from utilities.valid import Valid as v
from handler.users import UserHandler as u
from handler.staff import StaffHandler as s


class PassResetHandler:

    def resetPassword(self, id):
        userHandler = u().getUserByEmailReset(id)
        staffHandler = s().getStaffByEidMain(id)
        if userHandler[0] == False:
            print('no user')
        else:
            print('there is a user')
            return pr().addToResetTable(id, v().generateRandomString())
        if staffHandler[0] == False:
            print('no staff')
        else:
            return pr().addToResetTable(id, v().generateRandomString())

    def getReset(self, id):
        user = pr().retrieveFromResetTable(id)
        userHandler = u().getUserByEmailReset(user)
        staffHandler = s().getStaffByEidMain(user)
        if userHandler[0] == False:
            print('no user')
        else:
            return user, 'user'
        if staffHandler[0] == False:
            print('no staff')
        else:
            return user, 'staff'