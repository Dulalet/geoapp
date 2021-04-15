import ntpath
import os
import tempfile
import zipfile
from pathlib import Path
from random import random, randint

import geopandas as gpd
import geopandas.geodataframe
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from shapely.geometry import Point

from geo.importshp import normalize_gdf

RANDOM_POINTS = 3

def buffer_generate(pointX, pointY, radius, objectsGDF, from_file):
    # streetsGDF = gpd.read_file('//home/daulet/Desktop/WGS2/geojson/Улицы_Project.shp.geojson')
    # inputPoint = Point(7959830.520, 6643715.849)
    inputPoint = Point(pointX, pointY)
    if from_file is False:
        objectsGDF = normalize_gdf(objectsGDF)
    intersectionGeoSeries = objectsGDF.intersection(inputPoint.buffer(radius))
    for i in range(len(intersectionGeoSeries)):
        if intersectionGeoSeries[i].is_empty:
            intersectionGeoSeries.pop(i)

    intersectionsGDF = gpd.GeoDataFrame(gpd.GeoSeries(intersectionGeoSeries))
    intersectionsGDF = intersectionsGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
    # intersectionsGDF.plot()

    geomList = intersectionsGDF.geometry.to_list()
    randomPoints = []
    if len(geomList) == 0:
        return randomPoints
    for i in range(RANDOM_POINTS):
        randNum = randint(0, len(geomList)-1)
        randomPoints.append(geomList[randNum].interpolate(random(), True))
        randomPoints[i] = randomPoints[i].to_wkt()

    # plot random points:
    # xs = [point.x for point in randomPoints]
    # ys = [point.y for point in randomPoints]
    # plt.scatter(xs, ys)
    points = intersectionsGDF.boundary
    # points.to_json()
    # intersectionsGDF = gpd.GeoDataFrame(gpd.GeoSeries(points))
    # intersectionsGDF = intersectionsGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
    # intersectionsGDF.plot()
    # plt.show()
    return points, randomPoints

