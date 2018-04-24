from handler.staff import StaffHandler as s


class StaffTester:

    def printStaff(item):
        print('-----------------')
        print('Name:' + str(item['staff_fname']) + " " + str(item['staff_lname']))
        print('Email:' + str(item['staff_email']))
        print('Store:' + str(item['staff_store']))
        print('Administrator:' + str(item['admin']))

    print('==============================\nAll staff members in the database:\n==============================\n')
    staff = s().getAllStaff()
    for item in staff:
        printStaff(item)

    print('\n==============================\nAdding a new staff member:\n==============================\n')
    control = True
    eid = None
    # Validate eid #
    while (control):
        eid = input('EID:')
        if s().staffExists(eid):
            print('The staff member already exists!')
        else:
            control = False
    # Collect details #
    first = input("First Name:")
    last = input("Last Name:")
    email = input("Email:")
    store = input('Store:')
    control = True
    admin = None
    while (control):
        admin = input("Admin (y/n):")
        if admin == 'y' or admin == 'Y':
            admin = "True"
            control = False
        elif admin == 'n' or admin == 'N':
            admin = "False"
            control = False
        else:
            print('Only \'y\' (yes) or \'n\' (no)...')
    staff = {
        'first_name': first,
        'last_name': last,
        'eid': eid,
        'email': email,
        'store': store,
        'admin':admin
    }
    s().insertStaff(staff)
    print(
        '\n==============================\nThe staff member added was (Testing the getStaffbyEid function):\n==============================\n')
    staff = s().getStaffByEid(eid)

    printStaff(staff)
    # print('\n==============================\nAll users currently in the system are:\n==============================\n')
    # users = u().getAllUsers()
    # for item in users:
    #     printUsers(item)

    print('\n==============================\nUpdate Staff Administrator Status:\n==============================\n')
    control = True
    eid = None
    # Validate email address #
    while (control):
        eid = input('EID:')
        if s().staffExists(eid):
            ct = True
            admin = None
            while (ct):
                admin = input("Admin (y/n):")
                if admin == 'y' or admin == 'Y':
                    admin = True
                    ct = False
                elif admin == 'n' or admin == 'N':
                    admin = False
                    ct = False
                else:
                    print('Only \'y\' (yes) or \'n\' (no)...')
            s().updateStaffAsAdmin(eid, admin)
            control = False
        else:
            print('Staff EIS incorrect...')
    staff = s().getStaffByEid(eid)
    printStaff(staff)

    print('\n==============================\nUpdate Staff Email:\n==============================\n')
    eid = None
    control = True
    email = None
    # Validate email address #
    while (control):
        eid = input('Staff EID:')
        email = input('Email:')
        if not s().validEmail(email):
            print('Invalid email address!')
        if s().validEmail(email) and not s().staffExists(eid):
            print('The staff member does not exist!')
        elif s().validEmail(email) and s().staffExists(eid):
            control = False
    control = True
    s().updateStaffEmail(eid, email)
    staff = s().getStaffByEmail(email)
    print(
        "\n=============================\nUpdated Staff Member (Test getStaffByEmail):\n=============================\n")
    printStaff(staff)
    print('\n==============================\nUpdate User Password:\n==============================\n')
    control = True
    eid = None
    # Validate email address #
    while (control):
        eid = input('EID:')
        if s().validEmail(email) and not s().staffExists(eid):
            print('The staff member does not exist!')
        else:
            control = False
    oldPassword = None
    control = True
    while (control):
        oldPassword = input('Enter the current password:')
        if s().staffAuthenticate(eid, oldPassword):
            control = False
        else:
            print("The passwords do not match!")
    password = None
    control = True
    # Verify password #
    while (control):
        password = input('Password:')
        if s().validPassword(password):
            control = False
        else:
            print(
                'The password must be at least: 6 characters long, have 1 uppercase, 1 lowercase, and one special character ($, @, #)')
    s().updateStaffPassword(eid, oldPassword, password)
    staff = s().getStaffByEid(eid)
    printStaff(staff)

    print('\n==============================\nDelete Staff by EID:\n==============================')
    control = True
    while (control):
        eid = input('EID of staff member to delete:')
        if not s().staffExists(eid):
            print('The staff member does not exist!')
        else:
            control = False
    s().deleteStaff(eid)

    print(
        '\n==============================\nAll staff members currently in the system are:\n==============================\n')
    staff = s().getAllStaff()
    for item in staff:
        printStaff(item)
