from validate_email import validate_email
import string
from random import *
from passlib.hash import sha256_crypt


class Valid:

    def validPhone(self, phone):
        """
        Validates a phone number format.
        :param phone: The number to validate.
        :return: True if valid, False if not.
        """
        # Phone must be 10 digits long.
        if not phone.isdigit() or len(phone) < 10 or len(phone) > 10:
            return False
        else:
            return True

    def validZip(self, zip):
        """
        Validates a zip code format.
        :param zip: Zip code to validate.
        :return: True if valid, False if not.
        """
        # Zip must be 5 digits long.
        if not zip.isdigit() or len(zip) < 5 or len(zip) > 5:
            return False
        else:
            return True

    def validEmail(self, email):
        """
        Uses external library to validate email.
        :param email: Email to validate.
        :return: True if valid, False is not.
        """
        is_valid = validate_email(email)
        if is_valid:
            return True
        else:
            return False

    def validPassword(self, password):
        """
        Validates the format of a password to be compliant with the design specifications.
        :param password: The password to validate.
        :return: True if valid, fasle if not.
        """
        # Accepted symbols, at least one required.
        symbol = ['$', '@', '#', '%', '*', '?', '!']
        # too short.
        if len(password) < 8:
            return False
        # too long
        if len(password) > 15:
            return False
        # at least a digit
        if not any(char.isdigit() for char in password):
            return False
        # at least an uppercase letter.
        if not any(char.isupper() for char in password):
            return False
        # at least a lower case letter.
        if not any(char.islower() for char in password):
            return False
        # At least a symbol.
        if not any(char in symbol for char in password):
            return False
        return True

    def stringToBool(self, string):
        """
        Is the string a boolean expression.
        :param string: String to test.
        :return: True if 'true' or False if 'false'.s
        """
        string = self.toLower(string)
        if string == 'true':
            return True
        else:
            return False

    def isFloat(self, value):
        """
        Test if the string is a float.
        :param value: String to test.
        :return: True if float, False if not.
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def toUpper(self, string):
        """
        Make everything upper case.
        :param string: The string to edit.
        :return: All uppercase.
        """
        return string.upper()

    def toLower(self, string):
        """
        Make everything lower case.
        :param string: The string to edit.
        :return: All lowercase.
        """
        return string.lower()

    def generatePhotoName(self, extension):
        """
        Generates a random string for use as a photo name.
        :param extension: The real extension of the photo.
        :return: The new photo name with extension added.
        """
        minlength = 15
        maxlength = 25
        chars = string.ascii_letters + string.digits
        name = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return name + '.' + extension

    def encrypt(self, password):
        """
        Encrypt a string for use as a password.
        :param password: The string to encrypt.
        :return: Encrypted string for use in database as password..
        """
        return sha256_crypt.encrypt(password)

    def decrypt(self, testing, password):
        """
        Test a string with an encrypted one.
        :param testing: String to test, potential user password.
        :param password: The string from the database.
        :return: True if match, false if not.
        """
        return sha256_crypt.verify(testing, password)

    def generatePassword(self):
        """
        Generate a random string for use as a temporary password.
        :return: The temporary password.
        """
        minlength = 8
        maxlength = 12
        chars = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return password

    def generateRandomString(self):
        """
        Generate a random multipurpose string fro use in various parts of the website.
        :return:
        """
        minlength = 12
        maxlength = 25
        chars = string.ascii_letters + string.digits
        line = "".join(choice(chars) for x in range(randint(minlength, maxlength)))
        return line

    def sanitize(self, str):
        """
        Remove unwanted characters, spaces from string. Only accept letters and digits.
        :param str: String to sanitize.
        :return: Sanitized string.
        """
        whitelist = string.ascii_letters + string.digits
        newString = ''.join(c for c in str if c in whitelist)
        return newString

    def removeSpecialChars(self, str):
        """
        Removes symbols from strings and leaves only letters and digits, as well as spaces and dashes.
        :param str: String to filter.
        :return: Filtered string.
        """
        whitelist = string.ascii_letters + string.digits + ' ' + '-'
        newString = ''.join(c for c in str if c in whitelist)
        return newString

    def phoneStrip(self, str):
        """
        Removes characters from a phone number.
        :param str: String to filter
        :return: Filtered String
        """
        whitelist = string.digits
        newString = ''.join(c for c in str if c in whitelist)
        return newString
