from fastapi import FastAPI, HTTPException
from .mymodules import data_handling
from .mymodules import advanced_research
from .mymodules import air_quality
import pandas as pd

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
    except Exception as e:
        raise HTTPException(status_code=404, detail='Unfortunately we were not able to access OpenWheather API')


@app.get('/search')
def search_bnb(min, max, trees_bool, crime_rate ):
    min = int(min)
    max = int(max)
    crime_rate = int(crime_rate)
    zipcodes_attr = data_handling.corrZipAtt(min, max)
    zipcodes_trees = data_handling.corrZipTrees(trees_bool)
    zipcodes_crime = data_handling.corrZipCrime(crime_rate)


    if(zipcodes_attr and zipcodes_trees and zipcodes_crime):
        res = data_handling.commonZip(zipcodes_attr, zipcodes_crime, zipcodes_trees)

        val = data_handling.BnbPerZip(res, bnb)

        list_of_dicts = val.to_json(orient='records')

        return list_of_dicts
    else:
        return {"error": "Data not found"}


@app.get('/neighbourhood')
def get_borough(neighbourhood):
    data = data_handling.get_bnb_by_neighborhood(neighbourhood)
    if (type(data)==pd.DataFrame):
        if not(data.empty):
            list = data.to_json(orient='records')
            return list
    else:
        return {"error": "Data not found"}


@app.get('/advanced')
def airbnb_in_range(attractions, range):
    attractions = literal_eval(attractions)
    range = int(range)
    center_point = advanced_research.calculate_center(attractions)
    search_range = advanced_research.dist_to_deg(range, center_point)
    filtered_df = advanced_research.find_airbnb_in_range(center_point, search_range)
    list_of_dicts = filtered_df.to_json(orient = 'records')
    return list_of_dicts


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
