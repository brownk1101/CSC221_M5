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


import view_vetdb as view
import model_vetdb as model


def get_ownerID(owner_df):
    """
    retrieves owner ID from user and validates it
    :param owner_df: Pandas DataFrame: DataFrame that holds the owner
    information
    :return: ownerID: int: owner ID to use to search dataFrame
    """
    found = False
    while not found:
        id_to_validate = input("Please enter owner ID or press "
                                  "enter "
                               "to return to main menu: ")
        if id_to_validate == "":
            print("Returning to main menu")
            return None
        if int(id_to_validate) not in owner_df["OwnerId"].tolist():
            print("OwnerID not found")
            found = False
        else:
            return id_to_validate



def get_pet_breed(breed_list):
    """
    gets the pet breed from the user and validates it is in database
    :param: list: list of all breeds in vet clinic records
    :return: breed: str: name of pet breed to search for
    """


    view.display_breeds(breed_list)

    # Get breed from user
    while True:
        user_input = input("\nEnter the pet breed you would like "
                           "charges for \n").lower()
        matches = [breed for breed in breed_list if
                   user_input in breed.lower()]
        if not matches:
            print("No matching breeds found. Please try again.")
            continue

        # If one match, return it
        if len(matches) == 1:
            print(f"Selected breed: {matches[0]}")
            return matches[0]

        # If multiple matches, ask user to choose
        print("\nMultiple matches found:")
        for i, match in enumerate(matches, start=1):
            print(f"{i}) {match}")

        try:
            choice = int(input("Select the number of the breed: "))
            if 1 <= choice <= len(matches):
                return matches[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


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
            view.display_records(df_dict["OWNER"])
            model.write_to_csv(df_dict["OWNER"], "owner.csv")
        if menu_choice == 2:
            view.display_records(df_dict["PETS"])
            model.write_to_csv(df_dict["PETS"], "pets.csv")
        if menu_choice == 3:
            ownerID = get_ownerID(df_dict["OWNER"])
            fields = ["OwnerId", "OwnerFirstName", "OwnerLastName",
                       "OwnerPhone", "OwnerEmail" , "PetId", "PetName",
                       "PetBreed", "PetDOB"]
            if ownerID is not None:
                owner_df = model.create_owner_df(df_dict, ownerID)
                owner_name = owner_df["OwnerLastName"].iloc[0].lower()
                file_name = f'{owner_name}_{ownerID}.csv'
                model.write_to_csv(owner_df, file_name ,fields)
        if menu_choice == 4:
            ownerID = get_ownerID(df_dict["OWNER"])
            if ownerID is not None:
                owner_df = model.create_owner_df(df_dict, ownerID)
            fields = ("OwnerId", "OwnerFirstName", "OwnerLastName",
                      "OwnerEmail", "PetId", "PetName", "PetBreed",
                      "Service", "Date", "Charge")
            if ownerID is not None:
                owner_df = model.create_owner_df(df_dict, ownerID)
                charges = model.calculate_charges(owner_df)
                view.display_records(owner_df, fields)
                view.display_charges(charges, "owner")
        if menu_choice == 5:
            breed_list = model.get_breeds(df_dict["PETS"])
            breed = get_pet_breed(breed_list)
            breed_df = model.create_breed_df(breed, df_dict["PETS"])
            charges = model.calculate_charges(breed_df, "PetBreed")
            view.display_charges(charges, "breed", breed)
        if menu_choice == 6:
            view.display_exit()

if __name__ == "__main__":
    main()
