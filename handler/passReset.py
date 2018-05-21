from dao.passReset import PassResetDao as pr
from utilities.valid import Valid as v
from handler.users import UserHandler as u
from handler.staff import StaffHandler as s


class PassResetHandler:

    def resetPassword(self, id):
        """
        Generate a reset key for the user or staff/admin.
        :param id: The identifier of the user/staff/admin.
        :return: Returns the user id and the key that was generated.
        """
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
        """
        Retrieves key after reset link is accessed, deleted the key later.
        :param id: The identifier of the user.
        :return: The user dictionary and the type of user.
        """
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

    def getResetFromForms(self, id):
        """
        Generates the reset information for use in the forms.
        :param id: The identifier of the user/staff/admin
        :return: User dictionary with key and user type.
        """
        user = pr().generateAdminLinkReset(id)  # user devuelve lo que va a ser el link
        userHandler = u().getUserByEmailReset(id)
        staffHandler = s().getStaffByEidMain(id)
        if userHandler[0] == False:
            print('no user')
        else:
            return user, 'user'
        if staffHandler[0] == False:
            print('no staff')
        else:
            return user, 'staff'
