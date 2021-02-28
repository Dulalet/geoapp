import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection

from geo.models import Layer

gdf = gpd.read_file('/home/daulet/Desktop/WGS2/Улицы_Project.shp')  # import shp to a dataframe
geomList = gdf.geometry.to_list()  # make a list of objects from dataframe

# if geomList[0].type == 'Polygon':
#     for i in range(len(geomList)):
#         geomList[i] = geomList[i].wkt   # change types of objects in the list to wkt
#
#     list_polygons = [shapely.wkt.loads(poly) for poly in geomList]  # change types to shapely polygons
#
#     shapelyMultiPolygon = shapely.geometry.MultiPolygon(list_polygons)  # make multipolygon using shapely
#     shapelyMultiPolygon = shapelyMultiPolygon.wkt
#
#     geometry = GEOSGeometry(shapelyMultiPolygon, srid=3857)     # turn shapely multipolygon into geos multipolygon
#
# elif geomList[0].type == 'LineString':

for i in range(len(geomList)):
    geomList[i] = geomList[i].wkt
    geomList[i] = GEOSGeometry(geomList[i], srid=3857)
geometry = GeometryCollection(geomList)


layer = Layer()
layer.name = 'Улицы_Project'
layer.slug = 'streets'
layer.url = 'https://sacral.openlayers.kz/geo/streets/'
layer.data = gdf.to_json()
layer.geom = geometry
layer.save()

print("done")

# exec(open("geo/importshp.py").read()) this command is to run this file from shell
