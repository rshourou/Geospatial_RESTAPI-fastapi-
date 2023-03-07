from pydantic import BaseModel


class PropertyResponse(BaseModel):
    property_id: str
    geocode_geo: list(float)
    distance_m: float
