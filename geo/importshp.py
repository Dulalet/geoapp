import ntpath
import os
import tempfile
import zipfile
from pathlib import Path

import shapely
import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from geo.models import Layer
from geo.gpx2geopandas import importgpx


def gdf2layer(gdf, name, name_of_file, extension):
    geomList = gdf.geometry.to_list()  # make a list of objects from dataframe
    if len(geomList) > 1000:
        print("number of objects is 1000 max")
    geomList = geomList[0:1000]
    for i in range(len(geomList)):
        geomList[i] = shapely.wkb.loads(shapely.wkb.dumps(geomList[i], output_dimension=2))

        geomList[i] = geomList[i].wkt
        geomList[i] = GEOSGeometry(geomList[i], srid=3857)
    geometry = GeometryCollection(geomList)
    layer = Layer()
    layer.name = name_of_file.replace(extension, '')
    layer.slug = name
    layer.url = 'https://sacral.openlayers.kz/geo/' + layer.slug + '/'
    layer.type = geomList[0].geom_type
    layer.data = gdf.to_json()
    layer.geom = geometry
    layer.save()
    return layer


def importLayer(name, filepath):
    path = Path(filepath)
    name_of_file = ntpath.split(filepath)[1]
    extension = os.path.splitext(filepath)[1]
    if extension == '.zip':
        temp_dir = tempfile.TemporaryDirectory(dir=path.parent)
        print(temp_dir.name)
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)

        gdf = gpd.read_file(temp_dir.name + '/' + name_of_file[:-4] + '.shp')  # import shp to a dataframe
        temp_dir.cleanup()
        return gdf2layer(gdf, name, name_of_file, extension)
    elif extension == '.kml':
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
        gdf = gpd.read_file(filepath, driver='KML')
        return gdf2layer(gdf, name, name_of_file, extension)
    elif extension == '.csv':
        gdf = gpd.read_file(filepath)
        gdf.crs = 'epsg:3857'
        return gdf2layer(gdf, name, name_of_file, extension)
    elif extension == '.geojson':
        gdf = gpd.read_file(filepath)
        return gdf2layer(gdf, name, name_of_file, extension)
    # elif extension == '.gpx':
    #     gdf = importgpx(filepath)
    else:
        return Response('Error: not valid file type', HTTP_400_BAD_REQUEST)





# exec(open("geo/importshp.py").read()) this command is to run this file from shell
