from random import random

import geopandas as gpd
from shapely.geometry import Point

# p1 = Point((1, 2))
# p2 = Point((5, 6))
# df = pd.DataFrame({'a': [11, 22]})
# gdf = gpd.GeoDataFrame(df, geometry=[p1, p2])

streetsGDF = gpd.read_file('//home/daulet/Desktop/WGS2/geojson/Улицы_Project.shp.geojson')

inputPoint = Point(7959830.520, 6643715.849)

intersectionGeoSeries = streetsGDF.intersection(inputPoint.buffer(500))
for i in range(len(intersectionGeoSeries)):
    if intersectionGeoSeries[i].is_empty:
        intersectionGeoSeries.pop(i)

intersectionsGDF = gpd.GeoDataFrame(gpd.GeoSeries(intersectionGeoSeries))
intersectionsGDF = intersectionsGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
# intersectionsGDF.plot()

geomList = intersectionsGDF.geometry.to_list()
randomPoints = []
for i in range(3):
    randomPoints.append(geomList[i].interpolate(random(), True))

# plot random points:
# xs = [point.x for point in randomPoints]
# ys = [point.y for point in randomPoints]
# plt.scatter(xs, ys)

points = intersectionsGDF.boundary
intersectionsGDF = gpd.GeoDataFrame(gpd.GeoSeries(points))
intersectionsGDF = intersectionsGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
# intersectionsGDF.plot()
# plt.show()
