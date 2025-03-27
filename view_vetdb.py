"""
handles functions that allower user interactions for the vet clinic's
owner and pet database
"""

def display_menu(menu_options, size, ):
    """
    displays menu for user
    :param menu_options: list of strings that show menu options
    :param size: int: size of longest menu option plus size for menu
    header.
    :return: None
    """

    print("\nVet Clinic Pet Owner's Database")
    print("_"* size)
    for option in menu_options:
        print(option)

def get_menu_choice(total_options):
    """
    gets and validated users menu choice
    :param total_options: int: number of menu options
    :return: menu_choice: int: menu option user chose
    """

    while True:
        #prompt user for menu choice
        menu_choice = int(input(f'\nPlease select a valid menu option '
                                f'(1-{total_options})\n'))

        # Test if menu choice is valid
        if 0 < menu_choice <= total_options:
            return menu_choice


def display_records(df, columns = ("all",)):
    """
    Displays the data from a dataframe
    :param df pandas DataFrame: a DataFrame
    :param columns: list: the columns to display defaults tuple("all")
    if no columns provided.
    :return: None
    """
    print('\n' * 3)
    if columns[0] == "all":
        print(df)
    else:
        print(df[list(columns)])


def display_charges(charges, charge_type, breed=None):
    """
    displays charges for either an owner or breed
    :param charges: list: a list that holds a dict of pets and their
    charges, a sum of all charges, and an average for charges.
    :param type: str: clarifies if charges are for an owner or breed
    :param breed: str: breed name, is no argument breed=None
    :return: None
    """

    # Print the charges for an Owner's pet(s) and the sum of all
    # charges for that owner
    if charge_type == "owner":
        print('\nCharges for each pet are as follows:')
        print("_" * 40)
        for pet, charge in (charges[0]).items():
            print (f'{pet +":":<23}  ${charge:.2f}')
        print("_" * 40)
        print(f'Total charges for owner: ${charges[1]:.2f}\n\n\n')

    # Print the total charges for the breed and the average charge
    else:
        print(f"\n Total Charge for all {breed}s: {charges[1]}.")
        print(f"\n Average charge for a {breed}: {charges[2]}\n")

def display_breeds(breed_list):
    """
    prints
    :param breed_list:
    :return:
    """

    # Display all breeds available
    print(f'\nAvailable Breeds:\n')
    for index, breed in enumerate(breed_list, start=1):
        print(f"{breed:<20}", end='  ')
        if index % 3 == 0:
            print()
    if len(breed_list) % 3 != 0:
        print()

def display_exit():
    """
    displays exiting message
    :return:
    """

    print("Exiting owner information")