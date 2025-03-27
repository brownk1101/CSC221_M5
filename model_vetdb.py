"""Holds the model functions for the vet clinic's owner and pet
information database"""

import sqlite3 as db
import pandas as pd


def extract_database(file_name, table_names):
    """
    extracts data from a dataframe and write it to a DataFrame
    :param file_name: str: name of database file
    :param table_names: list: list of tables in dataframe
    :return: df_dict: a dictionary that holds the DataFrames created
    from
    a database
    """

    df_dict = {}
    try:
        # connect to database
        connection = db.connect(file_name)
        cursor = connection.cursor()

        # create a DataFrame for each table in the database
        for table in table_names:
            cursor.execute(f'SELECT * FROM {table}')
            rows = cursor.fetchall()

            # Get column names from table
            column_names = [description[0] for description in
                            cursor.description]

            # Create DataFrame for table
            df = pd.DataFrame(rows, columns=column_names)
            df_dict[table] = df
        connection.close()
    except db.DatabaseError as e:
        print(f"Database error {e}")
    except Exception as e:
        print(f"Unexpected error extracting data: {e}")
    return df_dict


def get_table_names(file_name):
    """
    get the names of all tables in a database
    :param file_name: str: name of database file
    :return: tables: list: list of table names
    """


    try:
        # connect to database
        connection = db.connect(file_name)
        cursor = connection.cursor()

        # get table names
        cursor.execute("Select name FROM sqlite_master Where type='table';")
        rows = cursor.fetchall()
        tables = []

        # add each table name to list
        for row in rows:
            tables.append(row[0])
        connection.close()
        return tables
    except db.DatabaseError as e:
        print(f"Failed to get table names: {e}")
        return []


def create_owner_df(df_dict, owner_id=None):
    """
    create a pandas dataframe specific to an owner and it's pets
    :param df_dict: dict: the owner and pet dictionary
    :param owner_id: int: owner ID to filter by, defaults None
    :return: owner_df: Pandas Dataframe: dataframe holding owner and
    it's pets data
    """


    # combine the owner and pet DataFrame based on d
    merged_df = pd.merge(df_dict["OWNER"], df_dict["PETS"],
                         on='OwnerId', how='inner')
    if owner_id is not None:
        merged_df = merged_df[merged_df["OwnerId"] == int(owner_id)]
    return merged_df


def write_to_csv(df, csv_name, columns=("all",)):
    """
    writes a dataframe to a csv file
    :param df: pandas DataFrame: the DataFrame to write to the CVS file
    :param csv_name: str: name for csv file
    :param columns: list: list of columns from the DataFrame to write to
     the CSV file, default= ("all",)
    :return: None
    """

    try:
        if columns[0] == "all":
            df.to_csv(csv_name, index=False)
            print(f"{csv_name} created")
        else:
            df.to_csv(csv_name, columns=list(columns), index=False)
            print(f"{csv_name} created")
    except KeyError as e:
        print(f"Column error: {e}")
    except Exception as e:
        print(f"Failed to write to CSV: {e}")


def calculate_charges(df, group_by_col="PetName"):
    """
    Calculate total charges for each pet, sum of charges for all
    pets, and average charge.
    :param df: a dataframe with data needed to calculate charges
    :param group_by_col: str: column name to group by default is
    PetName
    :return: charges_dict: dict: dictionary of each pet and it's total
    charges, sum_of_charge: int: total charge for customer,
    avg_charge: int: average charge across pets

    >>> import pandas as pd
    >>> data = {'PetName': ['Fluffy', 'Fluffy', 'Spike'], 'Charge': [
    ... 100, 200, 150]}
    >>> df = pd.DataFrame(data)
    >>> calculate_charges(df)
    ({'Fluffy': 300, 'Spike': 150}, 450, 225.0)
    """

    try:
        # calculate charges for a group
        group_charges = df.groupby(group_by_col)['Charge'].sum()

        # make a dict from grouped charges
        charges_dict = group_charges.to_dict()

        # Calculate sum of charges
        sum_of_charges = group_charges.sum()

        # Calculate average
        avg_charge = sum_of_charges/len(group_charges) if len(
            group_charges) > 0 else 0

        return charges_dict, sum_of_charges, avg_charge
    except KeyError as e:
        print(f"Missing column in DataFrame: {e}")
        return {}, 0, 0
    except Exception as e:
        print(f"Failed to calculate charges: {e}")
        return {}, 0, 0


def get_breeds(pet_df):
    """
    gets tuple of pet breeds from pets DataFrame
    :param pet_df: Pandas DataFrame: dataframe that holds all the
    pets in a vet clinics records
    :return: list: a list of pet breeds

    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'PetId': [1, 2, 3, 4],
    ...     'PetName': ['Fido', 'Mittens', 'Spike', 'Bella'],
    ...     'PetBreed': ['Beagle', 'Tabby', 'Beagle', 'Bulldog']
    ... })
    >>> get_breeds(df)
    ('Beagle', 'Tabby', 'Bulldog')
    """

    breed_list = pet_df['PetBreed'].unique().tolist()
    return breed_list

def create_breed_df(breed, pet_df):
    """

    :param breed: str: name of breed
    :param pet_df: DataFrame that holds pet data
    :return: breed_df: pandas DataFrame: Dataframe with data for a
    specific breed
    """

    breed_df = pet_df[pet_df["PetBreed"].str.lower() ==
                      breed.lower()]
    return breed_df


if __name__ == "__main__":
    import doctest
    doctest.testmod()