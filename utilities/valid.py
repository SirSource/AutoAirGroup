from validate_email import validate_email
import string
from random import *


class Valid:

    def validPhone(self, phone):

        if not phone.isdigit() or len(phone) < 10 or len(phone) > 10:
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
        symbol = ['$', '@', '#', '%', '*', '?', '!']
        if len(password) < 8:
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

    def stringToBool(self, string):
        string = self.toLower(string)
        if string == 'true':
            return True
        else:
            return False

    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def toUpper(self, string):
        return string.upper()

    def toLower(self, string):
        return string.lower()

    def generatePhotoName(self, extension):
        minlength = 15
        maxlength = 25
        chars = string.ascii_letters + string.digits
        name = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return name + '.' + extension
