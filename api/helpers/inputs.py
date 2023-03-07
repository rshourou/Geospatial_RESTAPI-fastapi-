
from pydantic import BaseModel

class LocationGeoJson(BaseModel):
    type: str
    coordinates: list[float]

class GeoJsonBody(BaseModel):
    location: LocationGeoJson
    distance: float
