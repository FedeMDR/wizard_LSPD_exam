import time
import requests
import json

CACHE_FILE = "air_quality_cache.json"
CACHE_EXPIRATION_TIME = 3600  # 1 hour in seconds

def air_quality(key : str):
    '''
    Get the most recent value of AQI for the five NYC neighbourhood

    Arg: 
        key (int) : the OpenWheather API key to access the API.
    
    Returns:
        list : list of five dictionaries with the AQI value for each neighbourhood of NYC.
    '''
    current_date = str(int(time.time()))

    neigh = {'Bronx': (40.844784, -73.864830),
             'Manhattan': (40.783058, -73.971252),
             'Queens': (40.728226, -73.794853),
             'Brooklyn': (40.678177, -73.944160),
             'Staten Island': (40.5834557, -74.1496048)}

    # Try to load cached data
    try:
        with open(CACHE_FILE, 'r') as cache_file:
            cached_data = json.load(cache_file)
    except (FileNotFoundError, json.JSONDecodeError):
        cached_data = {}

    airquality = []

    for neighborhood, coordinates in neigh.items():
        lat = str(coordinates[0])
        lon = str(coordinates[1])

        cache_key = f"{lat}_{lon}"
        cached_entry = cached_data.get(cache_key, None)

        # Check if cached data is available and not expired
        if cached_entry and (time.time() - cached_entry['timestamp']) <= CACHE_EXPIRATION_TIME and key == cached_entry['key']:
            mean_aqi = cached_entry['mean_aqi']
            quality = air_quality_status(mean_aqi)
        else:
            request = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start=946702800&end={current_date}&appid={key}'
            response = requests.get(request)
            json_data = response.json()
            aqi_values = [entry['main']['aqi'] for entry in json_data['list']]
            mean_aqi = sum(aqi_values) / len(aqi_values)
            quality = air_quality_status(mean_aqi)

            # Update cache
            cached_data[cache_key] = {'timestamp': time.time(), 'mean_aqi': mean_aqi, 'key':key}

        neighborhood_dict = {'Neighborhood': neighborhood, 'AQI': round(mean_aqi, 3), 'Quality': quality}
        airquality.append(neighborhood_dict)

    # Save updated cache
    with open(CACHE_FILE, 'w') as cache_file:
        json.dump(cached_data, cache_file)

    return airquality


def air_quality_status(aqi : int):
    '''
    For each value of AQI it returns the corresponding label based on the OpenWeather notation (https://openweathermap.org/api/air-pollution)

    Arg:
        aqi (int) : the AQI value retrived from OpenWeather API.
    '''
    if aqi <= 1:
        quality = 'Good'
    elif aqi<=2:
        quality = 'Fair'
    elif aqi<=3:
        quality =  'Moderate'
    elif aqi<=4:
        quality = 'Poor'
    else:
        quality = 'Very Poor'

    return quality