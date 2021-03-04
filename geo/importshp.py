import ntpath
import os
import tempfile
import zipfile
from pathlib import Path

import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection

from geo.models import Layer


def importLayer(name, filepath):
    path = Path(filepath)
    if (os.path.splitext(filepath)[1]) == '.zip':
        temp_dir = tempfile.TemporaryDirectory(dir=path.parent)
        print(temp_dir.name)
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)
        name_of_file = ntpath.split(filepath)[1]

        gdf = gpd.read_file(temp_dir.name + '/' + name_of_file[:-4] + '.shp')  # import shp to a dataframe
        geomList = gdf.geometry.to_list()  # make a list of objects from dataframe
        if len(geomList) > 1000:
            print("number of objects is 1000 max")
        geomList = geomList[0:1000]

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
        layer.name = name_of_file
        layer.slug = name
        layer.url = 'https://sacral.openlayers.kz/geo/' + layer.slug + '/'
        layer.type = geomList[0].geom_type
        layer.data = gdf.to_json()
        layer.geom = geometry
        layer.save()

        temp_dir.cleanup()

    elif (path[1]) == '.kml':
        pass

    print("done")
    return layer

# exec(open("geo/importshp.py").read()) this command is to run this file from shell
