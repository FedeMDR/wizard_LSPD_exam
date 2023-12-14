import pandas as pd
import math

AIRBNB = pd.read_csv('Datasets/AirBnb.csv')
ATTRACTION = pd.read_csv('Datasets/Location.csv')
EARTH_RADIUS = 6378137  # Earth's radius in meters
CIRCUMFERENCE = 2 * math.pi * EARTH_RADIUS  # Earth's circumference in meters


class GeoCoords:
    '''
    Class representing geographic coordinates.

    Example:
        To create an instance with valid coordinates:
        >>> location = GeoCoords(37.7749, -122.4194)
    '''
    def __init__(self, latitude: float, longitude: float):
        '''
        Initializes a GeoCoords object with the given latitude and longitude.

        Arg:
            latitude (float): The latitude value in the range [-90, 90].
            longitude (float): The longitude value in the range [-180, 180].

        Raises:
            ValueError: If the provided latitude or longitude
            value sare outside the valid ranges.
        '''
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("Invalid latitude or longitude values")
        self.latitude = latitude
        self.longitude = longitude


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


# converting price of our datasets from string to float
AIRBNB['price'] = AIRBNB['price'].apply(convert_price)


def calculate_center(selected_attractions: str):
    '''
    Calucalte the mean latitude and mean longitude of a given list of
    coordinates, to compute the center point.

    Arg:
        selected_attraction (str): a list of selected attractions, subset
        of the attractions in Location.csv.

    Returns:
        GeoCoords object : latitude and longitude of the center point
        stored in a GeoCoords object.
    '''
    df = ATTRACTION

    # Filter the data for selected attractions
    filtered_df = df[df['Tourist_Spot'].isin(selected_attractions)]

    # Calculate the average latitude and longitude
    center_latitude = filtered_df['Latitude'].mean()
    center_longitude = filtered_df['Longitude'].mean()

    return GeoCoords(center_latitude, center_longitude)


def is_within_range(lat: float, lon: float, center: GeoCoords, range: float):

    '''
    Checks if a given set of latitude and longitude is inside a given
    range from a given center

    Args:
        lat (float) : latitude of the location we want to check.
        lon (float) : longitude of the location we want to check.
        center (GeoCoords object) : the geographical coordinates
                                    of the central point of our
                                    search_area returned by the function
                                    "calculate_center".
        range (float) : the range of our search_area in degrees.

    Returns:
        bool : True if the given coordinates are inside the given area.
        bool : False if the given coordinates are outside the given area.
    '''
    return center.latitude - range <= lat <= center.latitude + range and \
        center.longitude - range <= lon <= center.longitude + range


def dist_to_deg(dist: int, center: GeoCoords):
    '''
    Compute the degree variation in latitude that correspond to the
    meters inputted. This result will be used as the search_range in
    the function "find_airbnb_in_range".

    Args:
        dist (int) :    distance in meters that correspond to
                        the radius of the search_area.
        center (GeoCoords object) : the geographical coordinates of the
                                    central point of our search_area returned
                                    by the function "calculate_center".

    Returns:
        float : the degree variation in latitude
                converted from the meters inputed.
    '''
    # compute conversion factor cirucmference of the earth * cos(latitude) / 360
    conversion_factor = CIRCUMFERENCE * math.cos(math.radians(center.latitude)) / 360
    var_degree = dist / conversion_factor

    return var_degree


def find_airbnb_in_range(center: GeoCoords, range: float):
    '''
    check which Airbnbs in our dataset (AirBnb.csv) are in the given range.

    Args:
        center (GeoCoords object) : the geographical coordinates of the central
                                    point of our search_area returned by the
                                    function "calculate_center".
        range (float) : the range of our search_area in degrees.

    Returns:
        pd.DataFrame :  A pandas dataframe containing only the Airbnb whose
                        coordinates fall inside the given range.
    '''
    filtered_airbnb = AIRBNB[AIRBNB.apply(lambda row: is_within_range(row['latitude'], row['longitude'], center, range), axis=1)]
    return filtered_airbnb


def get_attractions_list():
    '''
    extract the list of the names for each attraction
    in the attractionsdataframe ('Location.csv')

    Returns:
        list : attraction id and attraction name for each attraction
        in the Location.csv file so we can use it in a form.
    '''
    # Ottieni la lista delle attrazioni dal DataFrame
    attractions_list = ATTRACTION['Tourist_Spot'].tolist()
    return [(attraction, attraction) for attraction in attractions_list]
