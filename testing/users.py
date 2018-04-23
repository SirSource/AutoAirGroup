from handler.users import UserHandler as u


class UserTester:

    def printUsers(item):
        print('-----------------')
        print('Name:' + str(item['user_fname']) + " " + str(item['user_lname']))
        print('Email:' + str(item['user_email']))
        print('Phone:' + str(item['user_phone']))
        print('Address:' + str(item['place']) + "\n" + str(item['street']) + "\n" + str(item['city']) + ", P.R. " + str(
            item['zipcode']))

    print('==============================\nAll the users in he database:\n==============================\n')
    users = u().getAllUsers()
    for item in users:
        printUsers(item)

    print('\n==============================\nAdding a new user:\n==============================\n')
    control = True
    email = None
    # Validate email address #
    while (control):
        email = input('Email:')
        if not u().validEmail(email):
            print('Invalid email address!')
        if u().validEmail(email) and u().userExists(email):
            print('The email is valid, but a user already exists!')
        elif u().validEmail(email) and not u().userExists(email):
            control = False
    # Collect details #
    first = input("First Name:")
    last = input("Last Name:")
    phone = None
    control = True
    while (control):
        phone = input("Phone:")
        if u().validPhone(phone):
            control = False
        else:
            print('The phone number is not valid!')
    address1 = input('Address Line 1:')
    address2 = input('Address Line 2:')
    city = input('City:')
    zipcode = input('Zipcode:')
    password = None
    control = True
    # Verify password #
    while (control):
        password = input('Password:')
        if u().validPassword(password):
            control = False
        else:
            print(
                'The password must be at least: 6 characters long, have 1 uppercase, 1 lowercase, and one special character ($, @, #)')
    u().insertUser(first, last, 'customer', email, password, phone, city, address1, address2, zipcode)
    print(
        '\n==============================\nThe user added was (Testing the getUserByEmail function):\n==============================\n')
    users = u().getUserByEmail(email)
    print(users)
    print('\n==============================\nAll users currently in the system are:\n==============================\n')
    users = u().getAllUsers()
    for item in users:
        printUsers(item)



    print('\n==============================\nDelete a user by Email:\n==============================')
    control = True
    while (control):
        email = input('Email of user to delete:')
        if not u().validEmail(email):
            print('Invalid email address!')
        if u().validEmail(email) and not u().userExists(email):
            print('The email is valid, but a user does not exist!')
        elif u().validEmail(email) and u().userExists(email):
            control = False
    u().deleteUserByEmail(email)

    print('\n==============================\nAll users currently in the system are:\n==============================\n')
    users = u().getAllUsers()
    for item in users:
        printUsers(item)

