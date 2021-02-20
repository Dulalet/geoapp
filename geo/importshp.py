from django.contrib.gis.geos import GEOSGeometry
import geopandas as gpd
import shapely.wkt
import shapely.geometry

from geo.models import Layer

gdf = gpd.read_file('/home/daulet/Desktop/WGS2/Hydrography.shp')
geomList = gdf.geometry.to_list()

for i in range(len(geomList)):
    geomList[i] = geomList[i].wkt


list_polygons = [shapely.wkt.loads(poly) for poly in geomList]

shapelyMultiPolygon = shapely.geometry.MultiPolygon(list_polygons)
shapelyMultiPolygon = shapelyMultiPolygon.wkt

geometry = GEOSGeometry(shapelyMultiPolygon, srid=3857)

layer = Layer()
layer.name = 'hydro'
layer.data = gdf.to_json()
layer.geom = geometry
layer.save()

print("done")

# exec(open("geo/importshp.py").read()) this command is to run this file from shell
