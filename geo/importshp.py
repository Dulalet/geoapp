from django.contrib.gis.geos import GEOSGeometry
import geopandas as gpd
import shapely.wkt
import shapely.geometry

from geo.models import Layer

gdf = gpd.read_file('/home/daulet/Desktop/WGS2/Hydrography.shp')
geomList = gdf.geometry.to_list()
# l.save()
# tempStr = ""
# geomArr = []
#
# for i in geomString:
#     if i == 'P':
#         for j in range(geomString):
#
#         while i != "\n":
#             tempStr = tempStr + i
#             print(tempStr)
#             iter(i)
#         geomArr.extend(tempStr)
#         tempStr = ''
# print(geomArr)
#
#
# for i in range(geomString):
#     if geomString[i] == 'P':
#         j = i
#         while j != '\n':
#             tempStr = tempStr + i
#             print(tempStr)
#             j+=1
#         geomArr.extend(tempStr)
#         tempStr = ''
# print(geomArr)
#
# arr = geomString.split('\n')
# for i in range(len(arr)):
#     temp=arr[i][::]
#
# for i in range(1, 1000):
#     print(arr[0][i])

# print(geomList[0].wkt)
# a = geomList[0].wkt
# poly = GEOSGeometry(a, srid=3857)

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
