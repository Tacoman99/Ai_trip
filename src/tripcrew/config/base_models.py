from typing import List, Optional
from pydantic import BaseModel, Field


class Place_to_visit(BaseModel):
    place_name: str = Field(..., description="Name of the place")
    place_type: str = Field(..., description="Type of the place")
    place_description: str = Field(..., description="Description of the place")
    place_reason: str = Field(..., description="Reason for the recommendations")
    # make this optional  field
    place_latitude: float = Optional[Field(..., description=" Latitude of the place")]
    place_longitude: float = Optional[Field(..., description=" Longitude of the place")]
    place_sentiment: str = Optional[Field(..., description=" Overall sentiment of the reviews")]
    place_summary: str = Optional[Field(..., description=" Summary of the reviews")]


class City_guide(BaseModel):
    city_name: str = Field(..., description="Name of the city")
    places_to_visit: List[Place_to_visit] = Field(
        ..., description="List of places to visit in the city"
    )
