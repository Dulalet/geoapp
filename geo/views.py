import os

import psycopg2
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.db import connections
from rest_framework import viewsets, generics, permissions, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from geo.models import *
from geo.serializers import *
from geo.importshp import importLayer


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


# class addLayer(views.APIView):
#     queryset = LayerFile.objects.all()
#     serializer_class = UploadGeometrySerializer





@api_view(["POST"])
@permission_classes((AllowAny,))
def addLayer(request):
    serialized = UploadGeometrySerializer(data=request.data)
    print(serialized)
    if serialized.is_valid():
        media = os.getcwd()
        fs = FileSystemStorage(location=media+'/layer_files')
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.save()
        # import pdb
        # pdb.set_trace()
        geometry = importLayer(uploaded_file_url)
        serialized_geom = GeometrySerializer(geometry)
        return Response(serialized_geom.data)
    return Response('Error', HTTP_400_BAD_REQUEST)


