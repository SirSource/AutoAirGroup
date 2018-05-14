from dao.passReset import PassResetDao as pr
from utilities.valid import Valid as v
from handler.users import UserHandler as u
from handler.staff import StaffHandler as s


class PassResetHandler:

    def resetPassword(self, id):
        userHandler = u().getUserByEmailReset(id)
        staffHandler = s().getStaffByEidMain(id)
        print(userHandler)
        print(staffHandler)
        if userHandler[0] == False:
            print('no user')
        else:
            print('there is a user')
            return pr().addToResetTable(id, v().generatePassword())
        if staffHandler[0] == False:
            print('no staff')
        else:
            print('there is a staff')

    def getReset(self, id):
        user = pr().retrieveFromResetTable(id)
        print(user)