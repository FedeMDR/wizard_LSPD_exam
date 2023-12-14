from fastapi import FastAPI, HTTPException
from .mymodules import data_handling
from .mymodules import advanced_research
from .mymodules import air_quality
import pandas as pd
from fastapi import HTTPException
from ast import literal_eval

app = FastAPI()


# Creating dataframes with pandas
ATTRACTION = pd.read_csv('Datasets/Location.csv')
AIRBNB = pd.read_csv('Datasets/AirBnb.csv')


def convert_price(price_str):
    '''
    convert the price in Airbnb dataframe from a string to an integers

    Arg:
        price (str) : the price as a string
    
    Returns:
        int : the price converted to int
    '''
    prezzo_float = float(price_str.replace('$', '').replace(',', ''))

    return int(prezzo_float)

AIRBNB['price'] = AIRBNB['price'].apply(convert_price)


@app.get('/index/{key}')
def get_air_quality(key):
    '''
    endpoint to get the most recent airquality data.

    Args:
        key (str) : the API key for OpenWether service. 
    Returns: 
        list : a list of 5 dictionary with the AQI value for each neighbourhood of NYC.
    '''
    try:
        data = air_quality.air_quality(key)
        return data
    except Exception:
        raise HTTPException(status_code=404, detail='Unfortunately we were not able to access OpenWheather API')


@app.get('/search')
def search_bnb(min, max, trees_bool, crime_rate ):
    '''
    endpoint to query the airbnb based on number of attractions that the users want to visit, if the users want to stay close to green areas, and how much the users care about crimes.
    
    Args: 
        min (int) : the minimum amount of attraction that the user want to see.
        max (int) : the maximum amount of attractin that the user want to see.
        trees_bool (bool) : value that reflect if the user wants to stay in a green area or not.
        crime_rate (int) : a value from 1 to 4 given by the user depending on how much he cares about crimes.

    returns:
        list : all the airbnb and their data that match all the criteria given by the user
    '''
    
    #check if integer is between the correct range
    try:
        min = int(min)
        max = int(max)
        crime_rate = int(crime_rate)
        if not (1 <= crime_rate <= 4) or not (0 <= min <= 10) or not (5 <= max <=20):
            raise HTTPException(status_code=422, detail='Invalid crime rate. It must be between 0 and 5')
        else:
            zipcodes_attr = data_handling.corrZipAtt(min, max)
            zipcodes_trees = data_handling.corrZipTrees(trees_bool)
            zipcodes_crime = data_handling.corrZipCrime(crime_rate)
            res = data_handling.commonZip(zipcodes_attr, zipcodes_crime, zipcodes_trees)
            val = data_handling.BnbPerZip(res, AIRBNB)
            list_of_dicts = val.to_json(orient='records')

        return list_of_dicts
    except ValueError:
        raise HTTPException(status_code=404, detail='Unfortunatly we were not able to access OpenWheather API')

@app.get('/neighbourhood')
def get_borough(neighbourhood):
    '''
    Endpoint to query aibnbs based on the neighbourhood.

    Args: 
        neighbourhood (str) : the name of a neighbourhood of NYC.
    
    Returns:
        list : all the airbnb that are inside the given neighbourhood.
    '''

    try:
        data = data_handling.get_bnb_by_neighborhood(neighbourhood)
        list = data.to_json(orient='records')
        return list
    
    except Exception:
        raise HTTPException(status_code=404, detail='Input neighbourhood not valid')

@app.get('/advanced')
def airbnb_in_range(attractions, range):
    '''
    Endpoint to query the airbnbs inside a search area computed from the lists of attractions that the user want to visit.

    Args: 
        attractions (list) : the list of attractions selected by the user.
        range (int) : the radius of the search area in meters.
    
    Returns:
        list : all the airbnbs and their data that falls inside the search area.
    '''
    
    try:
        attractions = literal_eval(attractions)
        range = int(range)

        if not 100 <= range <= 100000:
            raise HTTPException(status_code=422, detail='Invalid distance range. It should be between 100m and 100km')
        else:
            center_point = advanced_research.calculate_center(attractions)
            search_range = advanced_research.dist_to_deg(range, center_point)
            filtered_df = advanced_research.find_airbnb_in_range(center_point, search_range)
            list_of_dicts = filtered_df.to_json(orient = 'records')
            return list_of_dicts
    
    except ValueError:
        raise HTTPException(status_code=404, detail='Invalid input type for distance range. It should be an integer')


@app.get('/map')
def get_map_data(attraction):
    '''
    Endpoint to get the latitude and longitude of all the selected attractions.

    Arg:
        attraction (list) : list of the attractions selected by the user.
    
    Returns:
        list : all the selected attractions and their coordinates data.
    '''
    attractions_list = literal_eval(attraction)
    extracted_attractions = ATTRACTION[ATTRACTION['Tourist_Spot'].isin(attractions_list)][['Tourist_Spot', 'Latitude', 'Longitude']]
    list_of_dicts = extracted_attractions.to_json(orient = 'records')
    return list_of_dicts


@app.get('/attractions')
def attraction_list():
    '''
    Endpoint to get the names of all the attractions from the attraction dataframe.

    Returns: 
        list : attraction id and attraction name for each attraction in the Location.csv file so we can use it in a form.
    '''
    attractions = advanced_research.get_attractions_list()

    return attractions