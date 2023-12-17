import pandas as pd

AIRBNB = pd.read_csv('Datasets/AirBnb.csv')
ATTRACTION = pd.read_csv('Datasets/Location.csv')
CRIME = pd.read_csv('Datasets/CrimeCount.csv')
TREES = pd.read_csv('Datasets/Trees.csv')
NEIGHBOURHOODS = ['Manhattan', 'Bronx', 'Queens', 'Staten Island', 'Brooklyn']


def convert_price(price_str: str):
    '''
    convert the price in Airbnb dataframe from a string to an integers

    Arg:
        price (str) : the price as a string

    Returns:
        int : the price converted to int
    '''
    prezzo_float = float(price_str.replace('$', '').replace(',', ''))

    return int(prezzo_float)


# Converting price of our datasets from string to float
AIRBNB['price'] = AIRBNB['price'].apply(convert_price)


# Finds zipcodes that respects the criteria for the number of attractions
def corr_zip_att(min: int, max: int):
    '''
    Count the number of attractions for each zipcodes and filters the zipcodes
    that have at leat {min} attractions and at most {max} attractions.

    Args:
        min (int) : the minimum amount of attraction that the user want to see.
        max (int) : the maximum amount of attractin that the user want to see.

    Returns:
        list :  list of the zipcodes that contains at least the
                number of attraction that the user want to see.
    '''
    counts_by_zipcode = ATTRACTION.groupby('Zipcode')['Tourist_Spot'].count().reset_index()
    filtered_locations = counts_by_zipcode[(counts_by_zipcode['Tourist_Spot'] >= min) &
                                           (counts_by_zipcode['Tourist_Spot'] <= max)]
    zipcodes_attr = filtered_locations['Zipcode'].tolist()

    return zipcodes_attr


# Finds zipcodes that respects the criteria for green areas
def corr_zip_trees(trees_bool: str):
    '''
    Compute the mean number of trees among all NYC neighbourhoods and
    return a list of zipcodes that match the user request.

    Arg:
        trees_bool (str) :  value that reflect if the user wants to stay
                            in a green area or not.

    Returns:
        list :
                if True :   all the zipcodes that have a number of trees that
                            is above the mean of NYC.
                if False :  returns every zipcodes.
    '''
    if trees_bool == 'True' or trees_bool == 'False':
        if (trees_bool == 'True'):
            trees_mean = int(TREES['count'].mean())
            zipcodes_trees = TREES[TREES['count'] >= trees_mean]['zipcode'].tolist()
            return zipcodes_trees
        elif (trees_bool == 'False'):
            zipcodes_trees = TREES['zipcode'].tolist()
            return zipcodes_trees
    else:
        raise ValueError()


# Finds zipcodes that respects the criteria for crime rates
def corr_zip_crime(crime_rate: int):
    '''
    Computes the crime rate threshold for
    each level of crime (from 1 to 4)

    Args:
        crime_rate (int) :  a value from 1 to 4 given by the
                            user depending on how much he cares about crimes.

    Returns:
        list :  a list of the zipcodes that comply
                with the crime level selected
    '''
    if (crime_rate == 4):
        crime_threshold = int(((CRIME['count'].max()-CRIME['count'].min())/4)+CRIME['count'].min())
        zipcodes_crime = CRIME[CRIME['count'] <= crime_threshold]['zipcode'].tolist()
    elif (crime_rate == 3):
        crime_threshold = int(((CRIME['count'].max()-CRIME['count'].min())/2)+CRIME['count'].min())
        zipcodes_crime = CRIME[CRIME['count'] <= crime_threshold]['zipcode'].tolist()
    elif (crime_rate == 2):
        crime_threshold = int(((((CRIME['count'].max()-CRIME['count'].min())/4))*3)+CRIME['count'].min())
        zipcodes_crime = CRIME[CRIME['count'] <= crime_threshold]['zipcode'].tolist()
    elif (crime_rate == 1):
        zipcodes_crime = CRIME['zipcode'].tolist()
    return zipcodes_crime


# Finds common zipcodes among three lists
def common_zip(zip_1: list, zip_2: list, zip_3: list):
    '''
    finds all the common zipcodes among the three given lists

    Args:
        zip_1 (list) : a list of zipcodes
        zip_2 (list) : a list of zipcodes
        zip_3 (list) : a list of zipcodes

    Returns :
        list : a list of the common zipcodes among the three lists
    '''
    res = set(zip_1) & set(zip_2) & set(zip_3)
    return list(res)


# Find the cheapest zipcode for each zipcode in the list
def bnb_per_zip(zip_list: list, bnb_df: pd.DataFrame):
    '''
    finds all the airbnb that are located inside a given zipcode

    Args:
        zip_list (list) : a list of zipcodes.
        bnb_df (pd.DataFrame) : A Dataframe containing at least
                                airbnbs and their zipcodes.

    Returns:
        pandas DataFrame :  a subset of our original dataframe
                            containing only the selected airbnbs
    '''
    airbnb_df = bnb_df[bnb_df['zipcode'].isin(zip_list)]

    return airbnb_df


def get_bnb_by_neighborhood(target_neighbourhood: str):
    '''
    Get all the airbnbs that are located inside the given neighbourhood.

    Args:
        Target_neighbourhoods (str) : a neighbourhood name

    Raises:
        ValueError :    if the target neighbourhood is empty
                        or is not a neighbourhood of NYC.

    Returns:
        padas DataFrame :   the first 50 airbnbs located
                            nside the given neighbourhood.

    '''
    if target_neighbourhood not in NEIGHBOURHOODS:
        target_neighbourhood = None
    if not target_neighbourhood:
        raise ValueError("Input must be a string and \
                         must be a NYC neighbourhood.")
    if target_neighbourhood in NEIGHBOURHOODS:
        neighborhood_df = AIRBNB[AIRBNB['neighbourhood_group_cleansed'] == target_neighbourhood]
        return neighborhood_df.head(50)
