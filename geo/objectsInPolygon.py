from shapely.geometry import Point


def numObjects(pointX, pointY, radius, objectsGDF, from_file):
    objectsList = objectsGDF.geometry.to_list()
    if from_file is False:
        objectsList = objectsList[0].geoms
    # inputPoint = Point(7959830.520, 6643715.849)
    inputPoint = Point(pointX, pointY)
    pointRadius = inputPoint.buffer(radius)
    inside = []
    for i in objectsList:
        if i.within(pointRadius):
            i = i.to_wkt()
            inside.append(i)
    return len(inside), inside
