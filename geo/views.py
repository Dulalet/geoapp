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


@api_view(["GET", "POST"])
@permission_classes((AllowAny,))
def ListWays(request):
    if request.method == 'GET':
        conn = connections['default']
        conn.ensure_connection()
        with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""select * from pgr_dijkstra(
            'select gid as id, source, target, cost from ways',
            1,
            346,
            directed := FALSE
            );""")
            row = cursor.fetchall()
        # query = Dijkstra.objects.filter(seq__in=row)
        serializer = DijkstraSerializer(row, many=True)
        print("QUERY: ", serializer.data)
        return Response(serializer.data)

    if request.method == 'POST':
        vertexSerializer = VertexSerializer(data=request.data)
        if vertexSerializer.is_valid():
            conn = connections['default']
            conn.ensure_connection()
            with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""select * from pgr_dijkstra(
                        'select gid as id, source, target, cost from ways',
                        {nodeFrom},
                        {nodeTo},
                        directed := FALSE
                        );""".format(nodeFrom=request.data["node_from"], nodeTo=request.data["node_to"]))
                row = cursor.fetchall()
            # query = Dijkstra.objects.filter(seq__in=row)
            serializer = DijkstraSerializer(row, many=True)
            print("QUERY: ", serializer.data)
            return Response(serializer.data)

            # post request accepts data in json format. For example:
            # {
            #     "node_from": "1",
            #     "node_to": "233"
            # }

    
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
        layer = importLayer(name=name, filepath=uploaded_file_url)
        serialized_layer = LayerSerializer(layer)
        fs.delete(file.name)
        return Response(serialized_layer.data)
    return Response('Error', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def countObjects(request):
    serialized = PointRadiusSerializer(data=request.data)
    print('serialized: ', serialized)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/layer_files')
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        # import pdb
        # pdb.set_trace()
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        objectsNum = numObjects(pointX, pointY, radius, uploaded_file_url)
        fs.delete(file.name)
        return Response(str(objectsNum))
    return Response('Error', HTTP_400_BAD_REQUEST)


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
        kpp_points, randomPoints = buffer_generate(pointX, pointY, radius, uploaded_file_url)
        fs.delete(file.name)
        return Response({'KPP': kpp_points.to_json(),
                         'Random Points': randomPoints})
    return Response('Error', HTTP_400_BAD_REQUEST)


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
        pointsDict = nearestPoints(pointX, pointY, radius, uploaded_file_url)
        fs.delete(file.name)
        return Response(json.dumps(pointsDict))
    return Response('Error', HTTP_400_BAD_REQUEST)


from geo.visibility_zones import get_visibility
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_visibility_zones(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/visibility_files')
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        # get_visibility(pointX, pointY, radius, uploaded_file_url)
        path = Path(uploaded_file_url)
        cmd = f"gdal_viewshed -md {radius} -ox {pointX} -oy {pointY} {uploaded_file_url} {path.parent}/out.tiff"
        os.system(cmd)
        return Response(str(path.parent) + '/out.tiff')
    return Response('error', HTTP_400_BAD_REQUEST)


