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


def display_owner_charges(charges):
    """
    displays the charges for an owner
    :param charges:  list that holds charges_dict: dict: dictionary of
    each pet and it's total charges, sum_of_charge: int: total charge
    for customer (not used in this function), and avg_charge: int:
    average charge across pets
    :return: None
    """
    print('\nCharges for each pet are as follows:')
    print("_" * 40)
    for pet, charge in charges[0].items():
        print(f'{pet + ":":<23}  ${charge:.2f}')
    print("_" * 40)
    print(f'Total charges for owner: ${charges[1]:.2f}\n\n\n')


def display_breed_charges(charges, breed):
    """
    displays the charges for a breed
    :param charges:  list that holds charges_dict: dict: dictionary of
    each pet and it's total charges, sum_of_charge: int: total charge
    for customer (not used in this function), and avg_charge: int:
    average charge across pets
    :param breed: str:  breed name to get charges for
    :return: None
    """
    print(f"\nTotal Charge for all {breed}s: ${charges[1]:.2f}")
    print(f"Average charge for a {breed}: ${charges[2]:.2f}\n")


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