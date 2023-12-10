import pandas as pd
import math
import json

#constants
AIRBNB = pd.read_csv('Datasets/AirBnb.csv')
ATTRACTION = pd.read_csv('Datasets/Location.csv')
EARTH_RADIUS = 6378137  # Earth's radius in meters
CIRCUMFERENCE = 2 * math.pi * EARTH_RADIUS  # Earth's circumference in meters

class GeoCoords:
    def __init__(self, latitude, longitude):
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("Invalid latitude or longitude values")
        self.latitude = latitude
        self.longitude = longitude

def convert_price(price_str):
    prezzo_float = float(price_str.replace('$', '').replace(',', ''))

    return int(prezzo_float)

AIRBNB['price'] = AIRBNB['price'].apply(convert_price)

def calculate_center(selected_attractions):
    '''
    calculate_center return the center point given the coordinates of different attractions

    Arg: 
    selected_attraction : list : str
        a list of all the selected attraction
    csv_file : str
        the path of the dataset containing the attractions name and their coordinates
    '''
    # Load data from CSV
    # df = pd.read_csv(csv_file)
    df = ATTRACTION
    # Filter the data for selected attractions
    filtered_df = df[df['Tourist_Spot'].isin(selected_attractions)]

    # Calculate the average latitude and longitude
    center_latitude = filtered_df['Latitude'].mean()
    center_longitude = filtered_df['Longitude'].mean()

    return GeoCoords(center_latitude, center_longitude)

def is_within_range(lat, lon, center, range):

    '''
    is_within_range checks if a given set of latitude and longitude is inside a given range from a given center

    Parameters
    ----------
    lat : float
        latitude of the location we want to check
    lon : float
        longitude of the location we want to check
    center : GeoCoords object
        the geographical coordinates of the central point of our search_area returned by the function "calculate_center"
    range : float
        the range of our search_area in degrees. 
    '''
    return center.latitude - range <= lat <= center.latitude + range and \
           center.longitude - range <= lon <= center.longitude + range

def dist_to_deg(dist, center):

    '''
    "dist_to_deg" will compute the degree variation in latitude that correspond to the meters inputted. 
    this result will be used as the search_range in the function "find_airbnb_in_range"

    Parameters
    ----------
    dist : int
        distance in meters that correspond to the radius of the search_area
    center : GeoCoords object
        the geographical coordinates of the central point of our search_area returned by the function "calculate_center"
    '''
    conversion_factor = CIRCUMFERENCE * math.cos(math.radians(center.latitude)) / 360
    var_degree = dist / conversion_factor

    return var_degree

def find_airbnb_in_range(center, range):
    filtered_airbnb = AIRBNB[AIRBNB.apply(lambda row: is_within_range(row['latitude'], row['longitude'], center, range), axis=1)]
    return filtered_airbnb


def get_attractions_list():    
    # Ottieni la lista delle attrazioni dal DataFrame
    attractions_list = ATTRACTION['Tourist_Spot'].tolist()
    return [(attraction, attraction) for attraction in attractions_list]