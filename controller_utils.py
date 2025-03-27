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


def handle_display_owners(df_dict):
    """
    handles the display owner option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """
    view.display_records(df_dict["OWNER"])
    model.write_to_csv(df_dict["OWNER"], "owner.csv")


def handle_display_pets(df_dict):
    """
    handles the display pets option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """
    view.display_records(df_dict["PETS"])
    model.write_to_csv(df_dict["PETS"], "pets.csv")


def handle_owner_search(df_dict):
    """
    handles the owner search option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """
    ownerID = get_ownerID(df_dict["OWNER"])
    fields = ["OwnerId", "OwnerFirstName", "OwnerLastName",
              "OwnerPhone", "OwnerEmail", "PetId", "PetName",
              "PetBreed", "PetDOB"]
    if ownerID is not None:
        owner_df = model.create_owner_df(df_dict, ownerID)
        owner_name = owner_df["OwnerLastName"].iloc[0].lower()
        file_name = f'{owner_name}_{ownerID}.csv'
        model.write_to_csv(owner_df, file_name, fields)


def handle_owner_charges(df_dict):
    """
    handles the display owner charges option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """
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
        view.display_owner_charges(charges)


def handle_breed_search(df_dict):
    """
    handles the breed search option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """
    breed_list = model.get_breeds(df_dict["PETS"])
    breed = get_pet_breed(breed_list)
    breed_df = model.create_breed_df(breed, df_dict["PETS"])
    charges = model.calculate_charges(breed_df, "PetBreed")
    view.display_breed_charges(charges, breed)


