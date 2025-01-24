from tools.google_api import GooglePlaces
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd
from config.config import settings




class google_places_input(BaseModel):
        """Input schema for google places tool"""
        query: str = Field(..., description="query to search  include location to search for places using google places api")
        radius: int = Field(50000, description="radius in meters to search for places using google places api")
        #area: str = Field(..., description="area to search for places using google places api e.g. San Diego, CA ")

class GooglePlacesTool(BaseTool):
    name: str = "Google Places Search Tool"
    description: str = "This tool is used to search for places using Google Places API"
    args_schema: Type[BaseModel] = google_places_input

    def __init__(self, query: str, radius: int):
        super().__init__()
        self.query = query
        self.radius = radius
        #self.area = area

    def _run(
              self, 
              query: str, 
              radius: int, 
              #area: str,
              ) -> pd.DataFrame:
   
        # Initialize GooglePlaces with the provided argument
        google_places = GooglePlaces(
             #area=self.area, 
             query=query, 
             radius=radius)

        # Fetch data
        merged_df = google_places.fetch_places()

        # Return the DataFrame as a string or any other format you need
        merged_df.to_csv(output_file=f'/home/jorger/travel-agent/ai-agents/data/{self.query}_reviews.csv',index=False) 
        
        return merged_df




    
    


    #c



# TODO: create this tool fully so the agent can use it to find places for the trip
#       - Ensuring the agent can do queries " Mexican restuarants", "Italian restaurants","Musuems in the area" etc 
#       - check for the struct array type for compression or flat structure


