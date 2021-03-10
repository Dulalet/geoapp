import ntpath
import os
import tempfile
import zipfile
from pathlib import Path
from random import random

import geopandas as gpd
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from shapely.geometry import Point


def buffer_generate(pointX, pointY, radius, filepath):
    # streetsGDF = gpd.read_file('//home/daulet/Desktop/WGS2/geojson/Улицы_Project.shp.geojson')
    # inputPoint = Point(7959830.520, 6643715.849)
    path = Path(filepath)
    name_of_file = ntpath.split(filepath)[1]
    extension = os.path.splitext(filepath)[1]
    if extension == '.zip':
        temp_dir = tempfile.TemporaryDirectory(dir=path.parent)
        print(temp_dir.name)
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)

        objectsGDF = gpd.read_file(temp_dir.name + '/' + name_of_file[:-4] + '.shp')  # import shp to a dataframe
        temp_dir.cleanup()
    elif extension == '.kml':
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
        objectsGDF = gpd.read_file(filepath, driver='KML')
    elif extension == '.csv':
        objectsGDF = gpd.read_file(filepath)
        objectsGDF.crs = 'epsg:3857'
    elif extension == '.geojson':
        objectsGDF = gpd.read_file(filepath)
    # elif extension == '.gpx':
    #     objectsGDF = importgpx(filepath)
    else:
        return Response('Error: cant read file', HTTP_400_BAD_REQUEST)

    inputPoint = Point(pointX, pointY)
    intersectionGeoSeries = objectsGDF.intersection(inputPoint.buffer(radius))
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

