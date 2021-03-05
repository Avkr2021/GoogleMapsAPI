import json
import requests
import time
import pandas as pd
import itertools
import datetime

API_KEY = '##'
API_SEARCH_URL_BASE = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


def request_api(url):
    response = requests.get(url)
    return response.status_code, response.json()

def get_places(type, pages=None, ciudad=None):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={type}+in+{ciudad}&region=.co&language=es&key={API_KEY}"
    results = []
    next_page_token = None

    if pages == None: 
        status, api_response = request_api(url)
        results += api_response['results']
        next_page_token = api_response.get("next_page_token", None)
        while next_page_token is not None: 
            page_url = f"{API_SEARCH_URL_BASE}?key={API_KEY}&pagetoken={next_page_token}"            
            status, api_response = request_api(str(page_url))
            results += api_response['results']
            next_page_token = api_response.get("next_page_token", None)
            time.sleep(5)
    else: 
        for num_page in range(pages):
            if num_page == 0:
                status, api_response = request_api(url)
                results += api_response['results']
            else:
                page_url = f"{API_SEARCH_URL_BASE}?key={API_KEY}&pagetoken={next_page_token}"   
                status, api_response = request_api(str(page_url))
                results += api_response['results']
                
            if api_response.get("next_page_token", None) is not None:
                next_page_token = api_response['next_page_token']
            else:
                break
            time.sleep(5)
    return results

def parse_info(place, type_name):
    return [
        place.get('name', None),
        place.get('business_status', None),
        place.get('formatted_address', None),
        place.get('place_id', None),
        place['geometry']['location']['lat'],
        place['geometry']['location']['lng'],
        place.get('rating', None),
        place.get('types', None),
        place.get('user_ratings_total', None),
        type_name       
    ]

def get_ciudad(ciudad, PLACE_TYPES):
    data = []
    for place_type in PLACE_TYPES:
        type_name = place_type[0]
        type_pages = place_type[1]
        result = get_places(type_name, type_pages, ciudad)
        time.sleep(5)
        result_parsed = list(map(lambda x: parse_info(x, type_name), result))
        data += result_parsed

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(f'info/{ciudad}-places-{str(datetime.datetime.today().date())}.csv')

CIUDADES = ["Bogota","Medellin", "Barranquilla", "Cartagena", "Cali"]
PLACES_TYPES = [("hospital", 4),("night+club", 4),
                   ("point+of+interes", 4), ("school", 4), 
                    ("transit+station",4), ("gym", 4), 
                    ("fire+station", 4), ("bank", 4), 
                    ("police", 4), ("restaurant", 4), 
                    ("shopping_mall", 4), ("stadium", 4), 
                    ("park", 4)]

[get_ciudad(ciudad, PLACES_TYPES) for ciudad in CIUDADES]

