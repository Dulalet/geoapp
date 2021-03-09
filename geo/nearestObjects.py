import geopandas as gpd
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import matplotlib.pyplot as plt
import psycopg2


def nearestPoints(inputPoint, filepath):
    # pointsGDF = gpd.read_file('//home/daulet/Desktop/WGS2/geojson/Остановки_Project1.shp.geojson')
    pointsGDF = gpd.read_file(filepath)
    pointsList = pointsGDF.geometry.to_list()

    inputPoint = Point(7959830.520, 6643715.849)
    pointRadius = inputPoint.buffer(500)

    inside = []
    distance = []
    # pointsDict = {}
    for point in pointsList:
        if point.within(pointRadius):
            # can be convenient to implement as a dict:
            # pointsDict[point] = point.distance(inputPoint)
            inside.append(point)
            distance.append(point.distance(inputPoint))

    # origGDF = gpd.GeoDataFrame(gpd.GeoSeries(inside))
    # origGDF = origGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
    # origGDF.plot()
    # plt.show()


