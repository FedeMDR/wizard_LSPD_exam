import pandas as pd

# Creating dataframes with pandas
attractions = pd.read_csv('Datasets/Location.csv')
crime = pd.read_csv('Datasets/CrimeCount.csv')
stations = pd.read_csv('Datasets/Stations.csv')
trees = pd.read_csv('Datasets/Trees.csv')
zip = pd.read_csv('Datasets/zip_neighbourhood.csv')
bnb = pd.read_csv('Datasets/AirBnb.csv')

def convert_price(price_str):
    prezzo_float = float(price_str.replace('$', '').replace(',', ''))

    return int(prezzo_float)

bnb['price'] = bnb['price'].apply(convert_price)


# Finds zipcodes that respects the criteria for the number of attractions
def corrZipAtt(min, max):
    # if(min>=0 and max<=20):
    counts_by_zipcode = attractions.groupby('Zipcode')['Tourist_Spot'].count().reset_index()
    filtered_locations = counts_by_zipcode[(counts_by_zipcode['Tourist_Spot'] >= min) & (counts_by_zipcode['Tourist_Spot'] <= max)]
    zipcodes_attr = filtered_locations['Zipcode'].tolist()
    
    return zipcodes_attr


# Finds zipcodes that respects the criteria for green areas
def corrZipTrees(trees_bool):
    if trees_bool == 'True' or trees_bool == 'False':
        if(trees_bool == 'True'):
            trees_mean = int(trees['count'].mean())
            zipcodes_trees = trees[trees['count'] >= trees_mean]['zipcode'].tolist()
            return zipcodes_trees
        elif(trees_bool == 'False'):
            zipcodes_trees = trees['zipcode'].tolist()
            return zipcodes_trees
    else:
        raise ValueError()


# Finds zipcodes that respects the criteria for crime rates
def corrZipCrime(crime_rate):
    # if isinstance(crime_rate, int):
        # if(crime_rate>=1 or crime_rate<=4):
            if(crime_rate == 4):
                crime_threshold = int(((crime['count'].max()-crime['count'].min())/4)+crime['count'].min())
                zipcodes_crime = crime[crime['count'] <= crime_threshold]['zipcode'].tolist()
            elif(crime_rate == 3):
                crime_threshold = int(((crime['count'].max()-crime['count'].min())/2)+crime['count'].min())
                zipcodes_crime = crime[crime['count'] <= crime_threshold]['zipcode'].tolist()
            elif(crime_rate == 2):
                crime_threshold = int(((((crime['count'].max()-crime['count'].min())/4))*3)+crime['count'].min())
                zipcodes_crime = crime[crime['count'] <= crime_threshold]['zipcode'].tolist()
            elif(crime_rate == 1):
                zipcodes_crime = crime['zipcode'].tolist()
            return zipcodes_crime
        # else:
        #     raise ValueError("Input crime_rate must be an integer.")
    


# Finds common zipcodes among three lists
def commonZip(zip_1, zip_2, zip_3):
    res = set(zip_1) & set(zip_2) & set(zip_3)
    return list(res)
    

# Find the cheapest zipcode for each zipcode in the list
def BnbPerZip(zip_list, bnb_df):
    airbnb_df = bnb_df[bnb_df['zipcode'].isin(zip_list)]
    
    return airbnb_df


def get_bnb_by_neighborhood(target_neighborhood):
    neighborhood_list = ['Manhattan', 'Bronx', 'Queens', 'Staten Island', 'Brooklyn']
    if target_neighborhood not in neighborhood_list:
        target_neighborhood == None
    if not target_neighborhood:
        raise ValueError("Input must be a string.")
    if target_neighborhood in neighborhood_list:
        neighborhood_df = bnb[bnb['neighbourhood_group_cleansed'] == target_neighborhood]
        return neighborhood_df.head(50)
    
