import googlemaps
from typing import Type, Optional
import pandas as pd 
import requests
from config.config import settings

class GooglePlaces:
    def __init__(
                self,  
                query: str, 
                radius: int,
                area: Optional[str] = None,  # Added a comma here
                ):
        
            """Initialize the GooglePlaces class

            Args:
                settings (dict): Configuration dictionary
                area (str): Area to search for places
                query (str): Query to search for places
                radius (int): Radius to search for places
            """
            self.settings = settings
            self.area = area
            self.query = query
            self.radius = radius
            self.API_KEY = settings.gcp_key
            self.search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"

        #gmaps = googlemaps.Client(key=self.API_KEY)
            #geocode_result = gmaps.geocode(self.area)

            #self.location = f"{geocode_result[0]['geometry']['location']['lat']}, {geocode_result[0]['geometry']['location']['lng']}"

    def _get_place_details(self, place_id):
        """Get place details from Google Places API

        Args:
            place_id (str): Place ID

        Returns:
            list: List of reviews
        """
        details_params = {
            'place_id': place_id,
            'fields': 'reviews',
            'key': self.API_KEY
        }
        details_response = requests.get(self.details_url, params=details_params)
        details_result = details_response.json().get('result', {})

        return details_result.get('reviews', [])

    def fetch_places(self):
        """Fetch places from Google Places API

        Returns:
            tuple: Tuple containing two pandas DataFrames (places and reviews)
        """
        data = []
        reviews = []
        params = {
            #'location': self.location,
            'radius': self.radius,
            'query': self.query,
            'key': self.API_KEY
        }
        while True:
            response = requests.get(self.search_url, params=params)
            results = response.json().get('results', [])
            next_page_token = response.json().get('next_page_token', None)

            #breakpoint()

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
                place_reviews = self._get_place_details(place['place_id'])
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
                ## Wait a few seconds before making the next request due to Google Places API limitations
                import time
                time.sleep(2)
            else:
                break
        # Create DataFrames
        df_places = pd.DataFrame(data)
        df_reviews = pd.DataFrame(reviews)
        merged_df = pd.merge(df_places, df_reviews, on='place_id', how='left')

        merged_df.to_csv(f"{'data'}_reviews.csv", index=False)

        return merged_df
    
if __name__ == "__main__":
    google_places = GooglePlaces(area="San Diego, CA", query="tacos in san diego", radius=5000)
    merged_df = google_places.fetch_places()
    print(merged_df)