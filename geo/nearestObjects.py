import ntpath
import os
import tempfile
import zipfile
from pathlib import Path

import geopandas as gpd
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from shapely.geometry import Point


def nearestPoints(pointX, pointY, radius, filepath):
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
    else:
        return Response('Error: cant read file', HTTP_400_BAD_REQUEST)

    # pointsGDF = gpd.read_file(filepath)
    # inputPoint = Point(7959830.520, 6643715.849)
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


