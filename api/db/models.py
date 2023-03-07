from typing import TypedDict

from .db import Base
from sqlalchemy import  Column, Float, String, PickleType
from geoalchemy2 import Geography


class PropertySerialized(TypedDict):
    id: str
    geo_code: str
    geocode_geo: str
    parcel_geo: str
    building_geo: str
    building_geo: str
    image_url: str


class Property(Base):
    __tablename__ = 'properties'
    id = Column(String, primary_key=True, index=True)
    geocode_geo = Column(Geography('POINT'))
    parcel_geo = Column(Geography('POLYGON'))
    building_geo = Column(Geography('POLYGON'))
    # image_bounds = Column([Float])
    image_url = Column(String)


    @property
    def serialize(self) -> PropertySerialized:
        return {
            'id': self.id,
            'geocode_geo': str(self.geocode_geo),
            'parcel_geo': str(self.parcel_geo),
            'building_geo': str(self.building_geo),
            'image_url': str(self.image_url),
        }
