from fastapi import FastAPI
from .mymodules import data_handling
from .mymodules import advanced_research
import pandas as pd
import requests
import time
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


@app.get('/search')
def search_bnb(min, max, trees_bool, crime_rate ):
    min = int(min)
    max = int(max)
    crime_rate = int(crime_rate)
    zipcodes_attr = data_handling.corrZipAtt(min, max)
    zipcodes_trees = data_handling.corrZipTrees(trees_bool)
    zipcodes_crime = data_handling.corrZipCrime(crime_rate)
    
    res = data_handling.commonZip(zipcodes_attr, zipcodes_crime, zipcodes_trees)

    val = data_handling.BnbPerZip(res, bnb)

    list_of_dicts = val.to_json(orient='records')

    return list_of_dicts

@app.get('/neighbourhood')
def get_borough(neighbourhood):
    data = data_handling.get_bnb_by_neighborhood(neighbourhood)
    list = data.to_json(orient='records')
    return list

@app.get('/index')
def air_quality():
    neigh = {'Bronx' : (40.844784,-73.864830),
             'Manhattan' : (40.783058, -73.971252),
             'Queens' : (40.728226, -73.794853),
             'Brooklyn' : (40.678177, -73.944160),
             'Staten Island' : (40.5834557, -74.1496048)
            }
    airquality = []
    for neighborhood, coordinates in neigh.items():
        
        lat = str(coordinates[0])
        lon = str(coordinates[1])
        current_date = str(int(time.time()))
        request = 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat='+ lat + '&lon=' + lon + '&start=946702800&end='+ current_date + '&appid=596dff3ac05aeb906e63803d2bfcf01a'
        response = requests.get(request)
        json = response.json()
        aqi_values = [entry['main']['aqi'] for entry in json['list']]
        mean_aqi = sum(aqi_values) / len(aqi_values)
        if mean_aqi <= 1:
            quality = 'Good'
        elif mean_aqi<=2:
            quality = 'Fair'
        elif mean_aqi<=3:
            quality =  'Moderate'
        elif mean_aqi<=4:
            quality = 'Poor'
        else:
            quality = 'Very Poor'

        neighborhood_dict = {'Neighborhood': neighborhood, 'AQI': round(mean_aqi, 3), 'Quality': quality}

        airquality.append(neighborhood_dict)

    return airquality

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


