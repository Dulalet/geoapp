import json
import os
from pathlib import Path

import psycopg2
from django.core.files.storage import FileSystemStorage
from django.db import connections
from django.http import HttpResponse
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from geo.buffer import buffer_generate
from geo.importshp import importLayer
from geo.nearestObjects import nearestPoints
from geo.objectsInPolygon import numObjects
from geo.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateBuilding(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class ListBuilding(generics.ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class UpdateBuilding(generics.RetrieveUpdateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class DeleteBuilding(generics.DestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class CreateBusStop(generics.ListCreateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


class ListBusStop(generics.ListAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


class UpdateBusStop(generics.RetrieveUpdateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


class DeleteBusStop(generics.DestroyAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


class CreateRedLine(generics.ListCreateAPIView):
    queryset = RedLine.objects.all()
    serializer_class = RedLineSerializer


class ListRedLine(generics.ListAPIView):
    queryset = RedLine.objects.all()
    serializer_class = RedLineSerializer


class UpdateRedLine(generics.RetrieveUpdateAPIView):
    queryset = RedLine.objects.all()
    serializer_class = RedLineSerializer


class DeleteRedLine(generics.DestroyAPIView):
    queryset = RedLine.objects.all()
    serializer_class = RedLineSerializer


class CreateStreet(generics.ListCreateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class ListStreet(generics.ListAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class UpdateStreet(generics.RetrieveUpdateAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class DeleteStreet(generics.DestroyAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class CreateHeatmap(generics.ListCreateAPIView):
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


class ListHeatmap(generics.ListAPIView):
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


class UpdateHeatmap(generics.RetrieveUpdateAPIView):
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


class DeleteHeatmap(generics.DestroyAPIView):
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


# @api_view(["GET", "POST"])
@api_view(["POST"])
@permission_classes((AllowAny,))
def ListWays(request):
    # if request.method == 'GET':
    #     conn = connections['default']
    #     conn.ensure_connection()
    #     with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
    #         cursor.execute("""select * from pgr_dijkstra(
    #         'select gid as id, source, target, cost from ways',
    #         1,
    #         5,
    #         directed := FALSE
    #         );""")
    #         row = cursor.fetchall()
    #     # query = Dijkstra.objects.filter(seq__in=row)
    #     serializer = DijkstraSerializer(row, many=True)
    #     return Response(serializer.data)

    # if request.method == 'POST':
    vertexSerializer = VertexSerializer(data=request.data)
    if vertexSerializer.is_valid():
        conn = connections['default']
        conn.ensure_connection()
        # print('from: ', vertexSerializer.data['closest_source']['geometry'])
        # print('to: ', vertexSerializer.data['closest_destination']['geometry'])
        with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""select * from pgr_dijkstra(
        'select gid as id, source, target, cost from ways',
        {node_from},
        {node_to},
        directed := FALSE
        );""".format(node_from=vertexSerializer.data['closest_source']['node'], node_to=vertexSerializer.data['closest_destination']['node']))
            row = cursor.fetchall()
        # query = Dijkstra.objects.filter(seq__in=row)
        serializer = DijkstraSerializer(row, many=True)
        print("QUERY: ", serializer.data)
        return Response(serializer.data)

    # UPDATE ways
    # SET barrier=TRUE
    # FROM (
    #          SELECT streets.gid AS gid, streets.the_geom AS geometry
    #          FROM ways streets
    #          WHERE ST_Intersects(streets.the_geom, 'SRID=4326;POINT(71.4691279 51.1247586)'::geometry) = TRUE
    # ) t
    # WHERE ways.gid = t.gid;
    #
    # -----------------------------------------------------
    #
    # select * from pgr_dijkstra(
    #         'select gid as id, source, target, cost from ways where ways.barrier=false',
    #         1,
    #         7,
    #         directed := FALSE
    # );

    
class GetLayer(generics.ListAPIView):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer


class UpdateLayer(generics.RetrieveUpdateAPIView):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer


@api_view(["POST"])
@permission_classes((AllowAny,))
def addLayer(request):
    serialized = UploadGeometrySerializer(data=request.data)
    if serialized.is_valid():
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/layer_files')
        name = serialized.validated_data['name']
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        serialized.save()
        try:
            layer = importLayer(name=name, filepath=uploaded_file_url)
            serialized_layer = LayerSerializer(layer)
        except ImportError:
            return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        finally:
            fs.delete(file.name)
        return Response(serialized_layer.data)
    return Response('Error', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def countObjects(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/layer_files')
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        try:
            objectsNum, objects = numObjects(pointX, pointY, radius, uploaded_file_url)
        except ImportError:
            return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        finally:
            fs.delete(file.name)
        return Response({'number of objects': str(objectsNum), 'objects': objects})
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def buffer(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/layer_files')
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        try:
            kpp_points, randomPoints = buffer_generate(pointX, pointY, radius, uploaded_file_url)
        except ImportError:
            return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        finally:
            fs.delete(file.name)
        return Response({'KPP': kpp_points.to_json(),
                         'Random Points': randomPoints})
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def showNearest(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/layer_files')
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        try:
            pointsDict = nearestPoints(pointX, pointY, radius, uploaded_file_url)
        except ImportError:
            return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        finally:
            fs.delete(file.name)
        return Response(json.dumps(pointsDict))
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


from geo.visibility_zones import get_visibility
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_visibility_zones(request):
    serialized = VisibilityZonesSerializer(data=request.data)
    if serialized.is_valid():
        observer_x = serialized.validated_data['observer_x']
        observer_y = serialized.validated_data['observer_y']
        observer_radius = serialized.validated_data['observer_radius']
        observer_height = serialized.validated_data['observer_height']
        file = serialized.validated_data['file']
        second_observer_x = serialized.validated_data['second_observer_x']
        second_observer_y = serialized.validated_data['second_observer_y']
        second_observer_radius = serialized.validated_data['second_observer_radius']
        second_observer_height = serialized.validated_data['second_observer_height']
        second_file = serialized.validated_data['second_file']

        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/visibility_files')
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        path = Path(uploaded_file_url)
        cmd = f"gdal_viewshed -md {observer_radius} -ox {observer_x} -oy {observer_y} -oz {observer_height} {uploaded_file_url} {path.parent}/out1.tiff"
        file_path = str(path.parent) + '/out1.tiff'
        os.system(cmd)
        if second_observer_x and second_observer_y and second_file:
            cmd = f"gdal_viewshed -md {second_observer_radius} -ox {second_observer_x} -oy {second_observer_y} -oz {second_observer_height} -vv 200 {uploaded_file_url} {path.parent}/out2.tiff"
            os.system(cmd)
            second_file_path = str(path.parent) + '/out2.tiff'
            result = get_visibility(file_path, second_file_path)
            fs.delete(file.name)
            fs.delete(second_file.name)
        else:
            result = get_visibility(file_path)
            fs.delete(file.name)
        return Response()
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


