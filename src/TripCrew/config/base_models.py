from typing import List
from pydantic import BaseModel, Field


class Place_to_visit(BaseModel):
    place_name: str = Field(..., description="Name of the place")
    place_type: str = Field(..., description="Type of the place")
    place_description: str = Field(..., description="Description of the place")
    place_reason: str = Field(..., description="Reason for the recommendations")


class City_guide(BaseModel):
    city_name: str = Field(..., description="Name of the city")
    places_to_visit: List[Place_to_visit] = Field(
        ..., description="List of places to visit in the city"
    )
