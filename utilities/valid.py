from validate_email import validate_email

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

    def stringToBool(self, string):
        if string == 'True':
            return True
        else:
            return False