"""
This program tracks pet and owner information at a veterinary clinic via
a database
Karen Brown
March 25, 2025
CSC-221 M5Pro

Pseudocode

Extract the vet_serv.db database into two dataframes
Display the following menu and continue to run program until user
chooses exit:
    1) Display OWNER content and create DataFrame
    2) Display PETS content and create DataFrame
    3) Retrieve Owner and Pet data for specific Owner
    4) Calculate Total Charge by Owner
    5) Retrieve Pet information by PetBreed
    6) Exit

If user chooses option 1, display the owner DataFrame and write
it to a csv file called owner.csv

If user chooses option 2, display the pets DataFrame and write it to
a csv file called pets.csv

If the user chooses option 3, prompt the user to enter the ownerID to
search. Display all records from both the owner and pet
DataFrame for that owner. The following fields will need to be
displayed: OwnerId, OwnerFirstName, OwnerLastName, OwnerPhone,
OwnerEmail ,PetId, PetName, PetBreed, PetDOB. Write this information
into a CSV file. The file should be names after the owner,
ex lastname_ownerID.csv.

If the user chooses option 4, prompt the user to enter the ownerID.
Display all records from both the owner and pet
DataFrame for that owner. The following fields will need to be
displayed: OwnerId, OwnerFirstName, OwnerLastName, OwnerEmail ,PetId,
PetName, PetBreed, Service, Date, Charge. Calculate the total charge
for each pet and sum of charges the owner. Display these charges for
the owner.

If the user chooses option 5, user the pets DataFrame to search for
specific breeds. Display a list of breads. Prompt the user for the
breed they wish to search for (will not be case-sensitive and allows
for partial search words). If multiple breeds retrieved for users
entry, display and allow user to pick one. Get all records for that
breed from the owner and pet DataFrame. Calculate the total charges
and over all averaged for that breed and display it.

If user chooses option 6, display "Exiting" and terminate the program.

"""


import model_vetdb as model
import view_vetdb as view
import controller_utils as ctrl

def main():
    """
    main function that displays menu and calls other functions for
    program
    :return: None
    """


    menu_options = [
        "1) Display OWNER content and create DataFrame",
        "2) Display PETS content and create DataFrame",
        "3) Retrieve Owner and Pet data for specific Owner",
        "4) Calculate Total Charge by Owner,",
        "5) Retrieve Pet information by PetBreed",
        "6) Exit"]
    size = len(max(menu_options, key=len)) + 6
    menu_choice = 0
    file_name = "vet_serv.db"
    tables = model.get_table_names(file_name)
    df_dict = model.extract_database(file_name, tables)
    while menu_choice != 6:
        view.display_menu(menu_options, size)
        menu_length = len(menu_options)
        menu_choice = view.get_menu_choice(menu_length)
        if menu_choice == 1:
            ctrl.handle_display_owners(df_dict)
        if menu_choice == 2:
            ctrl.handle_display_pets(df_dict)
        if menu_choice == 3:
            ctrl.handle_owner_search(df_dict)
        if menu_choice == 4:
           ctrl.handle_owner_charges(df_dict)
        if menu_choice == 5:
            ctrl.handle_breed_search(df_dict)
        if menu_choice == 6:
            view.display_exit()

if __name__ == "__main__":
    main()
