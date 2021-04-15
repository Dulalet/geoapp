import geopandas
from shapely.geometry import Point

from geo.importshp import normalize_gdf


def nearestPoints(pointX, pointY, radius, objectsGDF, from_file):
    # pointsGDF = gpd.read_file(filepath)
    # inputPoint = Point(7959830.520, 6643715.849)
    if from_file is False:
        objectsGDF = normalize_gdf(objectsGDF)
    pointsList = objectsGDF.geometry.to_list()
    inputPoint = Point(pointX, pointY)
    pointRadius = inputPoint.buffer(radius)

    inside = []
    distance = []
    for point in pointsList:
        if point.within(pointRadius):
            inside.append(point.to_wkt())
            distance.append(point.distance(inputPoint))
    pointsDict = dict(zip(inside, distance))
    return pointsDict

    # origGDF = gpd.GeoDataFrame(gpd.GeoSeries(inside))
    # origGDF = origGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
    # origGDF.plot()
    # plt.show()


