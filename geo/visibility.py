import shapely.geometry as shg
import matplotlib.pyplot as plt
import shapely.affinity as shaff
from functools import partial

import geopandas as gpd
# from pathlib import Path
import visilibity as vis
import numpy as np
from PIL import Image
from lgblkb_tools import logger, Folder
from lgblkb_tools.common.utils import run_cmd
from lgblkb_tools.gdal_datasets import DataSet
from lgblkb_tools.geometry import ThePoly, FieldPoly, ThePoint
# from lgblkb_tools.geometry.field_utils import generate_visible_poly
from lgblkb_tools.geometry.field_utils import epsilon
from lgblkb_tools.visualize import Plotter
# from osgeo import gdal
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation
from skimage.filters import threshold_otsu
# from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
from shapely.geometry import Polygon


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


def get_vis_env(polygon: FieldPoly):
    if polygon.is_clockwise: polygon = polygon.reversed
    vis_env = vis.Environment([polygon.vis_poly, *(x.vis_poly for x in polygon.holes)])
    assert vis_env.is_valid(epsilon)
    return vis_env


def makePoints(polygon):
    x_arr, y_arr = polygon.exterior.coords.xy
    points = []
    for j in range(len(x_arr)):
        points.append(vis.Point(x_arr[j], y_arr[j]))
    return points


def getXPoints(points):
    x_arr = []
    for point in points:
        x_arr.append(point.x())
    return x_arr


def getYpoints(points):
    y_arr = []
    for point in points:
        y_arr.append(point.y())
    return y_arr


epsilon = 0.0000001


@logger.trace()
def main():
    # FieldPoly.synthesize(50, hole_count=1).plot(c='red', alpha=0.3, lw=10) \
    #     .get_visible_poly(ThePoint([500, 500]).plot(c='k', lw=5)).plot()
    # plt.show()
    # return
    # work_folder = data_folder['dauka_tutorial_1']
    work_folder = Folder('/home/daulet/Desktop/zones')
    original_path = work_folder['4-3-1.tiff']
    logger.info("original_path: %s", original_path)
    original_ds = DataSet(original_path)

    orig_array = np.where(original_ds.array == -9999, np.nan, original_ds.array)
    orig_array = np.where(np.isnan(orig_array), np.nanmin(orig_array), orig_array)
    filtered_array = gaussian_filter(orig_array, sigma=1)
    otsu_threshold = threshold_otsu(filtered_array)
    mask = filtered_array > otsu_threshold
    eroded_mask = binary_erosion(mask, iterations=1)
    dilated_mask: np.ndarray = binary_dilation(eroded_mask, iterations=1).astype(int)
    # output to tiff
    # DataSet.from_array(dilated_mask, original_ds.geo_info) \
    #     .to_file(str(Path(original_path).with_name('output.tiff')), 'GTiff', no_data_value=0, dtype=gdal.GDT_Byte)
    geoms: gpd.GeoSeries = vectorize(dilated_mask, work_folder['vectorized.geojson'], original_ds)
    geom_extent = shg.Polygon(geoms.cascaded_union.envelope.boundary)
    # FieldPoly().bounds_xy
    # shg.Polygon(shg.Polygon().boundary)

    # for geom in geoms:
    #     geom_extent = geom_extent.difference(geom)
    # otirik_env = FieldPoly(geom_extent).plot(c='red')
    # # res = otirik_env.get_visible_poly(ThePoint(otirik_env.geometry.centroid)).plot(c='k').plot()
    # res = otirik_env.get_visible_poly(ThePoint([0, 0])).plot(c='k').plot()
    # # logger.info("res:\n%s", res)
    # # visible_zone.plot()
    # plt.show()

    print('!!!!!!!!!', geom_extent)

    # for i in range(len(geoms)):
    #     x_arr, y_arr = geoms[i].exterior.coords.xy
    #     holes = [[0] * len(x_arr)] * len(geoms)
    #     for j in range(len(x_arr)):
    #         holes[i][j] = vis.Point(x_arr[j], y_arr[j])
    #         holes_x = holes[i][j].x()

    vis_polygons = []
    x_arr = []
    y_arr = []
    for i in range(len(geoms)):
        points = makePoints(geoms[i])
        vis_polygons.append(vis.Polygon(points))
        x_arr.append(getXPoints(points))
        y_arr.append(getYpoints(points))
        print('Hole in standard form: ', vis_polygons[i].is_in_standard_form())
    points = makePoints(geom_extent)
    walls = vis.Polygon(points)
    # vis_polygons.insert(0, walls)
    env = vis.Environment([walls, vis_polygons[0]])

    print('Walls in standard form : ', walls.is_in_standard_form())
    print('Environment is valid : ', env.is_valid(epsilon))

    observer = vis.Point(673000, 5665000)
    observer.snap_to_boundary_of(env, epsilon)
    print('!!!!', vis_polygons, '!!!!!!')
    observer.snap_to_vertices_of(env, epsilon)

    # isovist = vis.Visibility_Polygon(observer, env, epsilon)






    # plotter = Plotter()
    # plotter.add_images(mask, eroded_mask, dilated_mask)
    # plotter.plot(lbrtwh=(1e-3, 1e-3, 1 - 1e-3, 1 - 1e-3, 1e-3, 0)).show()
    # return


if __name__ == '__main__':
    main()
