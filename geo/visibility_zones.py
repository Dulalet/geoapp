import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gp


import os
import stat
gdal_data = os.environ['GDAL_DATA']
print('is dir: ' + str(os.path.isdir(gdal_data)))
gcs_csv = os.path.join(gdal_data, 'gcs.csv')
print('is file: ' + str(os.path.isfile(gcs_csv)))
st = os.stat(gcs_csv)
print('is readable: ' + str(bool(st.st_mode & stat.S_IRGRP)))

mask = None
with rasterio.Env():
    with rasterio.open('/home/daulet/Desktop/zones/4-3-1.tif') as src:
        image = src.read(1)  # first band
        results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v)
            in enumerate(shapes(image, mask=mask, transform=src.transform)))

    geoms = list(results)
    print(geoms[0])

# gpd_polygonized_raster = gp.GeoDataFrame.from_features(geoms)


# https://gis.stackexchange.com/questions/187877/how-to-polygonize-raster-to-shapely-polygons/187883