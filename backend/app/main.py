from fastapi import FastAPI, HTTPException
from .mymodules import data_handling
from .mymodules import advanced_research
from .mymodules import air_quality
import pandas as pd
from fastapi import HTTPException
from ast import literal_eval

app = FastAPI()


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


@app.get('/index/{key}')
def get_air_quality(key):
    try:
        data = air_quality.air_quality(key)
        return data
    except Exception:
        raise HTTPException(status_code=404, detail='Unfortunately we were not able to access OpenWheather API')


@app.get('/search')
def search_bnb(min, max, trees_bool, crime_rate ):
    
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
            val = data_handling.BnbPerZip(res, bnb)
            list_of_dicts = val.to_json(orient='records')

        return list_of_dicts
    except ValueError:
        raise HTTPException(status_code=404, detail='Unfortunatly we were not able to access OpenWheather API')

@app.get('/neighbourhood')
def get_borough(neighbourhood):

    try:
        data = data_handling.get_bnb_by_neighborhood(neighbourhood)
        list = data.to_json(orient='records')
        return list
    
    except Exception:
        raise HTTPException(status_code=404, detail='Input neighbourhood not valid')

@app.get('/advanced')
def airbnb_in_range(attractions, range):
    
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
    attractions_list = literal_eval(attraction)
    print(attractions_list)
    extracted_attractions = attractions[attractions['Tourist_Spot'].isin(attractions_list)][['Tourist_Spot', 'Latitude', 'Longitude']]
    list_of_dicts = extracted_attractions.to_json(orient = 'records')
    return list_of_dicts


@app.get('/attractions')
def attraction_list():
    attractions = advanced_research.get_attractions_list()

    return attractions