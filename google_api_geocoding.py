import requests
import pandas as pd
API_KEY = '##'


def parse_response(res_json):
    location = res_json["results"][0]["geometry"]["location"]
    return (location["lat"], location["lng"])
    

def get_location(direction, ciudad):
    search = f"{direction},+{ciudad}".replace("#", "No")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={search}&language=es&region=CO&key={API_KEY}"
    response = requests.get(url)
    #print(response.json())
    if response.json()["status"] == "OK":
        latlong = parse_response(response.json())
    #print(response.json())
    else: 
        latlong = (None, None)
    return latlong


def make_lat_long(row):
    lat,log = get_location(row["direccion"], row["ciudad"])
    return pd.Series({'latitud':lat, 'longitud':log})


## Ejemplo uso:
## df[["direccion", "ciudad"]].apply(lambda row: make_lat_long(row), axis=1)