import ntpath
import os
from pathlib import Path


def get_visibility(pointX, pointY, distance, filepath):
    cmd = f"gdal_viewshed -md {distance} -ox {pointX} -oy {pointY} {filepath} out.tiff"
    os.system(cmd)
    print(Path('4-3-1.tiff'))