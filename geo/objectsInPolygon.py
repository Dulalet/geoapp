import geopandas as gpd
from shapely.geometry import Point


def countObjects(inputPoint, filename):
    buildingsGDF = gpd.read_file('//home/daulet/Desktop/WGS2/geojson/Здания_и_сооружения_Project.shp.geojson')
    buildingsList = buildingsGDF.geometry.to_list()

    inputPoint = Point(7959830.520, 6643715.849)
    pointRadius = inputPoint.buffer(500)

    inside = []
    for i in buildingsList:
        if i.within(pointRadius):
            inside.append(i)
            print("YES")
        else:
            print(".")
    print(inside)

    return len(inside)

# intersectionsGDF = gpd.GeoDataFrame(gpd.GeoSeries(intersectionGeoSeries))
# intersectionsGDF = intersectionsGDF.rename(columns={0: 'geometry'}).set_geometry('geometry')
