import requests
import time

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