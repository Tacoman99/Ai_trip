from crewai.tools import tool
from typing import Dict
import googlemaps
from datetime import datetime
from tabulate import tabulate

if __name__ == "__main__":

    import pandas as pd
    import requests
    from src.inputs import config
    # Replace with your API key
    API_KEY = config.gcp_key

    # Define search parameters
    location = "32.7157,-117.1611"  # Latitude,longitude San Diego
    radius = 150000  # Search radius in meters
    #search_type = "restaurant"  # limits search to restaurants
    keyword = "tacos"  # Restrict to gas stations
    

    # Define the base URL for the Places API
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        'location': location,
        'radius': radius,
        'keyword': keyword,
        'key': API_KEY  # Replace with your actual API key
    }   
    # Function to get place details and reviews
    def get_place_details(place_id):
        details_params = {
            'place_id': place_id,
            'fields': 'reviews',
            'key': API_KEY
        }
        details_response = requests.get(details_url, params=details_params)
        details_result = details_response.json().get('result', {})
        return details_result.get('reviews', [])

    # Function to handle paginated results
    def fetch_places(params):
        data = []
        reviews = []
        while True:
            response = requests.get(search_url, params=params)
            results = response.json().get('results', [])
            next_page_token = response.json().get('next_page_token', None)

            for result in results:
                place = {
                    'name': result.get('name'),
                    'business_status': result.get('business_status'),
                    'lat': result['geometry']['location']['lat'],
                    'lng': result['geometry']['location']['lng'],
                    'rating': result.get('rating'),
                    'user_ratings_total': result.get('user_ratings_total'),
                    'vicinity': result.get('vicinity'),
                    'price_level': result.get('price_level'),
                    'place_id': result.get('place_id'),
                }
                data.append(place)

                # Fetch place details to get reviews
                place_reviews = get_place_details(place['place_id'])
                for review in place_reviews:
                    reviews.append({
                        'place_id': place['place_id'],
                        'author_name': review.get('author_name'),
                        'rating': review.get('rating'),
                        'text': review.get('text'),
                        'time': review.get('time')
                    })

            if next_page_token:
                params['pagetoken'] = next_page_token
                # Esperar unos segundos antes de realizar la siguiente solicitud debido a limitaciones de la API de Google Places
                import time
                time.sleep(2)
            else:
                break

        return data, reviews

    # Fetch data
    data, reviews = fetch_places(params)

    # Create DataFrames
    df_places = pd.DataFrame(data)
    df_reviews = pd.DataFrame(reviews)



    #
    #print(tabulate(df, headers='keys', tablefmt='psql'))

    df_places.to_csv(f"{keyword}.csv", index=False)
    df_reviews.to_csv(f"{keyword}_reviews.csv", index=False)

# TODO: create this tool fully so the agent can use it to find places for the trip
#       - Ensuring the agent can do queries " Mexican restuarants", "Italian restaurants","Musuems in the area" etc 

