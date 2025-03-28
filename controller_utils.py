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
        try:
            id_input = input("Please enter owner ID or press enter "
                             "return to main menu: ")
            if id_input == "":
                print("Returning to main menu")
                return None
            id_to_validate = int(id_input)
            # Compare using string versions for safety
            owner_ids = owner_df["OwnerId"].astype(str).tolist()
            if str(id_to_validate) in owner_ids:
                return id_to_validate
            else:
                print("OwnerID not found")
        except ValueError:
            print("Please enter a valid numeric ID.")
        except Exception as e:
            print(f"Unexpected error: {e}")


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

    try:
        view.display_records(df_dict["OWNER"])

        # write the owner DataFrame to a csv file
        model.write_to_csv(df_dict["OWNER"], "owner.csv")
    except Exception as e:
        print(f"Error displaying or saving owner data: {e}")


def handle_display_pets(df_dict):
    """
    handles the display pets option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """

    try:
        view.display_records(df_dict["PETS"])

        # write the pets DataFrame to a csv file
        model.write_to_csv(df_dict["PETS"], "pets.csv")
    except Exception as e:
        print(f"Error displaying or saving pet data: {e}")


def handle_owner_search(df_dict):
    """
    handles the owner search option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """

    try:
        ownerID = get_ownerID(df_dict["OWNER"])
        if ownerID is None:
            return

        if ownerID not in df_dict["PETS"]["OwnerId"].tolist():
            print("This owner has no pet records.")
            return

        # create a DataFrame with only specific owner data
        owner_df = model.create_owner_df(df_dict, ownerID)

        if ownerID not in df_dict["PETS"]["OwnerId"].tolist():
            print("This owner has no pet records.")
            return

        fields = ["OwnerId", "OwnerFirstName", "OwnerLastName",
                  "OwnerPhone", "OwnerEmail", "PetId", "PetName",
                  "PetBreed", "PetDOB"]

        # get the owner name to use for file naming
        owner_name = owner_df["OwnerLastName"].iloc[0].lower()
        view.display_records(owner_df, fields)
        file_name = f'{owner_name}_{ownerID}.csv'

        # write the owner DataFrame to a csv file
        model.write_to_csv(owner_df, file_name, fields)
    except Exception as e:
        print(f"Error retrieving owner data: {e}")


def handle_owner_charges(df_dict):
    """
    handles the display owner charges option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """
    try:
        ownerID = get_ownerID(df_dict["OWNER"])
        if ownerID is None:
            return

        # Check if that owner has pets before merging
        if ownerID not in df_dict["PETS"]["OwnerId"].tolist():
            print("This owner has no pet records.")
            return

        owner_df = model.create_owner_df(df_dict, ownerID)

        fields = ["OwnerId", "OwnerFirstName", "OwnerLastName",
                  "OwnerPhone", "OwnerEmail", "PetId", "PetName",
                  "PetBreed", "PetDOB"]

        owner_name = owner_df["OwnerLastName"].iloc[0].lower()
        view.display_records(owner_df, fields)
        file_name = f"{owner_name}_{ownerID}.csv"
        model.write_to_csv(owner_df, file_name, fields)


    except Exception as e:
        print(f"Error retrieving owner data: {e}")


def handle_breed_search(df_dict):
    """
    handles the breed search option from menu
    :param df_dict: a dictionary that holds the DataFrames for Owners
    and Pets
    :return: None
    """

    try:

        # Get a list of all breeds in DataFrame
        breed_list = model.get_breeds(df_dict["PETS"])

        # Get the breed to search by
        breed = get_pet_breed(breed_list)

        # Create a DataFrame to hold all pets of a specific breed
        breed_df = model.create_breed_df(breed, df_dict["PETS"])

        # Calculate charges for that breed
        charges = model.calculate_charges(breed_df, "PetBreed")

        # Display charges for a specific breed
        view.display_breed_charges(charges, breed)
    except Exception as e:
        print(f"Error retrieving breed data: {e})")


