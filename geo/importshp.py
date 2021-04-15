import ntpath
import os
import tempfile
import zipfile
from pathlib import Path

import geopandas
import shapely
import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from geo.models import Layer


def gdf2layer(name, filepath, user):
    # gdf = gdf.truncate(after=999)
    gdf = importLayer(filepath)
    name_of_file = ntpath.split(filepath)[1]
    extension = os.path.splitext(filepath)[1]
    geomList = gdf.geometry.to_list()  # make a list of objects from dataframe
    if len(geomList) > 1000:
        print("number of objects is 1000 max")
        geomList = geomList[0:1000]
    for i in range(len(geomList)):
        geomList[i] = shapely.wkb.loads(shapely.wkb.dumps(geomList[i], output_dimension=3))

        if not geomList[i].has_z:
            geomList[i] = shapely.ops.transform(lambda x, y: (x, y, 0), geomList[i])

        geomList[i] = geomList[i].wkt
        geomList[i] = GEOSGeometry(geomList[i], srid=3857)
    geometry = GeometryCollection(geomList)
    layer = Layer()
    layer.name = name_of_file.replace(extension, '')
    layer.slug = name
    layer.url = 'https://sacral.openlayers.kz/geo/' + layer.slug + '/'
    layer.type = geomList[0].geom_type
    layer.data = gdf.to_json()
    layer.user = user
    if user.is_superuser:
        layer.is_general = True
    layer.geom = geometry
    try:
        layer.save()
    except Exception as e:
        print(e)
        # return Response('Could not save the file, it can be too long', HTTP_400_BAD_REQUEST)
        return None
    return layer


def importLayer(filepath):
    path = Path(filepath)
    name_of_file = ntpath.split(filepath)[1]
    extension = os.path.splitext(filepath)[1]
    if extension == '.zip':
        temp_dir = tempfile.TemporaryDirectory(dir=path.parent)
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir.name)

        gdf = gpd.read_file(temp_dir.name + '/' + name_of_file[:-4] + '.shp')  # import shp to a dataframe
        temp_dir.cleanup()
        # return gdf2layer(gdf, name, name_of_file, extension)
        return gdf
    elif extension == '.kml':
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
        gdf = gpd.read_file(filepath, driver='KML')
        # return gdf2layer(gdf, name, name_of_file, extension)
        return gdf
    elif extension == '.csv':
        gdf = gpd.read_file(filepath)  # can add separator "sep = ;"
        gdf.crs = 'epsg:3857'
        # return gdf2layer(gdf, name, name_of_file, extension)
        return gdf
    elif extension == '.geojson':
        gdf = gpd.read_file(filepath)
        # return gdf2layer(gdf, name, name_of_file, extension)
        return gdf
    else:
        return None


from sqlalchemy import create_engine
from geoapp.settings import DATABASES


def import_from_db(layerid):
    db_connection_url = f"postgresql://{DATABASES['default']['USER']}:{DATABASES['default']['PASSWORD']}" \
                        f"@{DATABASES['default']['HOST']}:{DATABASES['default']['PORT']}/{DATABASES['default']['NAME']}"
    con = create_engine(db_connection_url)
    sql = f"select * from geo_layer where id={layerid}"
    gdf = geopandas.read_postgis(sql, con)
    return gdf


def normalize_gdf(gdf):
    geoms = gdf.geometry.to_list()
    objectsGDF = geopandas.GeoDataFrame({'geometry': geoms[0].geoms})
    return objectsGDF

# exec(open("geo/importshp.py").read()) this command is to run this file from shell
