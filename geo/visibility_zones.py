import os
from functools import partial
from pathlib import Path

import geopandas as gpd
import numpy as np
import shapely.affinity as shaff
from PIL import Image
from lgblkb_tools import logger, Folder
from lgblkb_tools.common.utils import run_cmd
from lgblkb_tools.gdal_datasets import DataSet
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
    # считывание файла и создание numpy array из него:
    work_folder = Folder(filepath)
    original_path = work_folder[filepath]
    logger.info("original_path: %s", original_path)
    original_ds = DataSet(original_path)

    # удаление лишних пикселей:
    orig_array = np.where(original_ds.array == -9999, np.nan, original_ds.array)
    orig_array = np.where(np.isnan(orig_array), np.nanmin(orig_array), orig_array)
    filtered_array = gaussian_filter(orig_array, sigma=1)
    otsu_threshold = threshold_otsu(filtered_array)
    mask = filtered_array > otsu_threshold
    eroded_mask = binary_erosion(mask, iterations=5)
    filtered_mask: np.ndarray = binary_dilation(eroded_mask, iterations=5).astype(int)
    # geoms: gpd.GeoSeries = vectorize(orig_array>250, work_folder['vectorized.geojson'], original_ds)

    # создание векторной геометрии из numpy array:
    geoms: gpd.GeoSeries = vectorize(filtered_mask, work_folder['vectorized.geojson'], original_ds)

    # ----------------------------если расчет проводится для двух наблюдателей------------------------------
    if second_filepath is not None:
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
        # geoms2: gpd.GeoSeries = vectorize(orig_array2>250, work_folder2['vectorized2.geojson'], original_ds2)
        geoms2: gpd.GeoSeries = vectorize(filtered_mask2, work_folder2['vectorized2.geojson'], original_ds2)

    # --------------------------------------------------------------
        path = Path(filepath)
        # команды выполняющиеся в командной строке для создания растрового файла с обоюдной зоной видимости (GDAL>3.1.0)
        cmd = f"""cd {path.parent}
            gdal_translate out1.tiff out11.tiff -ot Int32
            gdal_translate out2.tiff out22.tiff -ot Int32
            gdal_merge.py -init "0 0" -o merged.tiff -ot Int32 out1.tiff out2.tiff
            gdal_calc.py -A merged.tiff --outfile=whitemerged.tiff --calc="A * 0" --type=Int32 --overwrite
            gdal_merge.py -init "0 0" -o merged1.tiff -ot Int32 whitemerged.tiff out1.tiff 
            gdal_merge.py -init "0 0" -o merged2.tiff -ot Int32 whitemerged.tiff out2.tiff
            gdal_calc.py -A merged1.tiff -B merged2.tiff --outfile=final.tiff --calc="A + B" --type=Int32 --overwrite
            rm merged.tiff whitemerged.tiff merged1.tiff merged2.tiff out1.tiff out2.tiff out11.tiff out22.tiff"""
        os.system(cmd)
        # получение финального файла с обоюдной зоной видимости
        work_folder3 = Folder(str(path.parent) + '/final.tiff')
        original_path3 = work_folder3[str(path.parent) + '/final.tiff']
        logger.info("original_path: %s", original_path3)
        original_ds3 = DataSet(original_path3)
        orig_array3 = np.where(original_ds3.array > 300, original_ds3.array, 0)
        orig_array3 = np.where(np.isnan(orig_array3), np.nanmin(orig_array3), orig_array3)
        filtered_array3 = gaussian_filter(orig_array3, sigma=1)
        otsu_threshold3 = threshold_otsu(filtered_array3)
        mask3 = filtered_array3 > otsu_threshold3
        eroded_mask3 = binary_erosion(mask3, iterations=1)
        filtered_mask3: np.ndarray = binary_dilation(eroded_mask3, iterations=1).astype(int)

        # geoms3: gpd.GeoSeries = vectorize(orig_array3>500, work_folder3['vectorized3.geojson'], original_ds3)

        # получение веторной геометрии для обоюдной зоны видимости
        geoms3: gpd.GeoSeries = vectorize(filtered_mask3, work_folder3['vectorized3.geojson'], original_ds3)

        return geoms, geoms2, geoms3
    return geoms
    # ----------вспомогательный код для визуализации и теста:---------------------------
    # print('!!!!!!!!!', geoms)
    # print('!!!!!!!!!', geoms2)
    # print('!!!!!!!!!', geoms3)
    # for geom in geoms3:
    #     plt.plot(*geom.exterior.xy, c='g', lw=3)
    # for geom in geoms2:
    #     plt.plot(*geom.exterior.xy, c='r', alpha=0.2)
    # for geom in geoms:
    #     plt.plot(*geom.exterior.xy, c='b', alpha=0.2)
    # plt.show()
    #
    # plotter = Plotter()
    # # plotter.add_images(mask, eroded_mask, dilated_mask)
    # plotter.add_images(mask, mask2, mask3, filtered_mask, filtered_mask2, filtered_mask3)
    # plotter.plot(lbrtwh=(1e-3, 1e-3, 1 - 1e-3, 1 - 1e-3, 1e-3, 0)).show()
    # return
    # ----------------------------------------------------------

if __name__ == '__main__':
    get_visibility('/home/daulet/Desktop/zones/out1.tiff', '/home/daulet/Desktop/zones/out2.tiff')
