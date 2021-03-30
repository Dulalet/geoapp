from functools import partial
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely.affinity as shaff
from PIL import Image
from lgblkb_tools import logger, Folder
from lgblkb_tools.common.utils import run_cmd
from lgblkb_tools.gdal_datasets import DataSet
from lgblkb_tools.visualize import Plotter
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation
from skimage.filters import threshold_otsu


def set_georeference(plain_geom, ds: DataSet, nrows=None):
    transform = ds.transform
    nrows = nrows or ds.array.shape[0]
    scaled_geom = shaff.scale(plain_geom, xfact=transform[1], yfact=abs(transform[5]), origin=(0, 0))
    out_geom = shaff.translate(scaled_geom, transform[0], transform[3] + transform[5] * nrows)
    return out_geom


def vectorize(mask, filepath, ds: DataSet, nrows=None):
    filepath = Path(filepath).with_suffix('.bmp')
    assert mask.min() == 0
    assert mask.max() == 1
    Image.fromarray(np.uint8(mask) * 255, 'L').save(filepath)
    vector_path = filepath.with_suffix('.geojson')
    run_cmd(f'potrace -b geojson --alphamax 0 -u 100 -i -o {vector_path} {filepath}', debug=True)
    image_geoms = gpd.GeoSeries(gpd.read_file(vector_path).geometry, crs=f"epsg:{ds.epsg}") \
        .map(partial(set_georeference, ds=ds, nrows=nrows))
    image_geoms.to_file(vector_path, driver='GeoJSON')
    return image_geoms


@logger.trace()
def get_visibility(filepath, second_filepath=None):
    work_folder = Folder(filepath)
    original_path = work_folder[filepath]
    logger.info("original_path: %s", original_path)
    original_ds = DataSet(original_path)

    orig_array = np.where(original_ds.array == -9999, np.nan, original_ds.array)
    orig_array = np.where(np.isnan(orig_array), np.nanmin(orig_array), orig_array)
    filtered_array = gaussian_filter(orig_array, sigma=1)
    otsu_threshold = threshold_otsu(filtered_array)
    mask = filtered_array > otsu_threshold
    eroded_mask = binary_erosion(mask, iterations=5)
    filtered_mask: np.ndarray = binary_dilation(eroded_mask, iterations=5).astype(int)

    geoms: gpd.GeoSeries = vectorize(filtered_mask, work_folder['vectorized.geojson'], original_ds)

    # ----------visualize and check:---------------------------
    print('!!!!!!!!!', geoms)
    for geom in geoms:
        plt.plot(*geom.exterior.xy)
    plt.show()

    plotter = Plotter()
    # plotter.add_images(mask, eroded_mask, dilated_mask)
    plotter.add_images(mask, filtered_mask)
    plotter.plot(lbrtwh=(1e-3, 1e-3, 1 - 1e-3, 1 - 1e-3, 1e-3, 0)).show()
    # return
    # ----------------------------------------------------------

    work_folder2 = Folder(second_filepath)
    original_path2 = work_folder2[second_filepath]
    logger.info("original_path: %s", original_path2)
    original_ds2 = DataSet(original_path2)

    orig_array2 = np.where(original_ds2.array == -9999, np.nan, original_ds2.array)
    orig_array2 = np.where(np.isnan(orig_array2), np.nanmin(orig_array2), orig_array2)
    filtered_array2 = gaussian_filter(orig_array2, sigma=1)
    otsu_threshold2 = threshold_otsu(filtered_array2)
    mask2 = filtered_array2 > otsu_threshold2
    eroded_mask2 = binary_erosion(mask2, iterations=5)
    filtered_mask2: np.ndarray = binary_dilation(eroded_mask2, iterations=5).astype(int)

    geoms2: gpd.GeoSeries = vectorize(filtered_mask2, work_folder2['vectorized2.geojson'], original_ds2)

    # ----------visualize and check:---------------------------
    print('!!!!!!!!!', geoms2)
    for geom in geoms2:
        plt.plot(*geom.exterior.xy)
    plt.show()

    plotter = Plotter()
    # plotter.add_images(mask, eroded_mask, dilated_mask)
    plotter.add_images(mask2, filtered_mask2)
    plotter.plot(lbrtwh=(1e-3, 1e-3, 1 - 1e-3, 1 - 1e-3, 1e-3, 0)).show()
    return
    # ----------------------------------------------------------



if __name__ == '__main__':
    get_visibility('/home/daulet/Desktop/zones/out1.tiff', '/home/daulet/Desktop/zones/out2.tiff')
