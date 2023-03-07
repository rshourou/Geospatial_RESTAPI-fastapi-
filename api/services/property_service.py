from shapely import wkb
from shapely.geometry import Point
from helpers.inputs import GeoJsonBody
from db.models import Property
import os.path
from client.client import download_image
from db.db import db_conn
from loguru import logger
from geopy.distance import great_circle
from sqlalchemy import func


class PropertyService():
    def __init__(self):
        PropertyService.__init__(self)
    
    @staticmethod
    def list_properties():
        logger.info('getting all properties')
        properties = db_conn.query(Property).all()        
        return [p.serialize for p in properties]

    @staticmethod
    def get_or_download_image(id):
        logger.info(f'Get or downloading image')
        file_name = f'/tmp/{id}.jpeg'
        if not os.path.isfile(file_name):
            property = db_conn.query(Property).filter(Property.id == id).first()
            download_image(property.image_url, file_name)
        return file_name

    @staticmethod
    def find_distance(geo_json: GeoJsonBody):
        logger.info(f'looking for distance {geo_json.__dict__}')
        geom = f'{geo_json.location.type.upper()}({geo_json.location.coordinates[0]} {geo_json.location.coordinates[1]})'

        properties = db_conn.query(Property).filter(func.ST_DWithin(Property.geocode_geo, geom, geo_json.distance, use_spheroid = True)).all()
        logger.info(f'properties {properties}')
        res_properties = []
        geom = Point((geo_json.location.coordinates[0], geo_json.location.coordinates[1]))
        for property in properties:
            point = wkb.loads(bytes(property.geocode_geo.data))
            distance_m = great_circle((point.x, point.y), geo_json.location.coordinates)
            logger.info(f'distance2 is {distance_m.meters}')

            res_properties.append({
                    'property_id': property.id,
                    'geocode_geo': str(point),
                    'distance_m': distance_m.meters        
            })
        return res_properties
    
    
    @staticmethod
    def statistics(id, zone):
        properties = []
        query_statitics = f"""
            SELECT 
              id,
                ST_Area(parcel_geo),
                ST_Area(building_geo),
                ST_Distance(geocode_geo, ST_Centroid(building_geo)),
                ST_Area(building_geo)/ST_Area(ST_Buffer(geocode_geo, {zone}))   
            FROM properties  AS p
            WHERE p.id = '{id}'
        """
        rows = db_conn.execute(query_statitics)
        for r in rows:
            properties.append({
                'id': r[0],
                'parcel_area_sqm': r[1],
                'building_area_sqm': r[2],
                'building_distance_m': r[3],
                'zone_density': r[4]
            })
        return properties