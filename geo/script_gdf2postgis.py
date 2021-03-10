from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import geopandas as gpd

engine = create_engine('postgresql://postgres:Cwau8JEumEZWDEPB@95.59.124.163:5455/mydatabase')
geodataframe = gpd.read_file('/home/daulet/Desktop/heatmap/geojson/Heatmap.geojson')

geodataframe.to_postgis(
    con=engine,
    name="heatmap",
    index="id",
    if_exists='replace'
)
