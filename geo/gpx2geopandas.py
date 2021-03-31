# import gpxpy, geopandas, json
# import matplotlib.pyplot as plt
# import datetime
# import numpy as np
# import pandas as pd
#
# from geopandas import GeoDataFrame
# from shapely.geometry import Point, LineString
#
#
# def gpx2df(gpx):
#     data = gpx.tracks[0].segments[0].points
#
#     ## Start Position
#     start = data[0]
#     ## End Position
#     finish = data[-1]
#
#     df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
#     for point in data:
#         df = df.append({'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation, 'time' : point.time}, ignore_index=True)
#     df['time'] = df['time'].astype(str).str[:-6]
#     df['time'] = pd.to_datetime(df['time'], dayfirst=True)
#     return data, df
#
#
# def importgpx(filepath):
#     gpx_file = open(filepath, 'r')
#     gpx = gpxpy.parse(gpx_file)
#
#     data, df = gpx2df(gpx)
#
#     geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
#     crs = {'init': 'epsg:4326'}
#     gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
#     gdf['entity_id'] = gdf.index
#
#     return gdf
