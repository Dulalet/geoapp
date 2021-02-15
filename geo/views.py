from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection, connections
from django.http import JsonResponse
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from geo.serializers import UserSerializer, GroupSerializer, BuildingSerializer, \
    BusStopSerializer, RedLineSerializer, StreetSerializer, WaySerializer
from geo.models import Building, BusStop, RedLine, Street, Way


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


# class ListWays(generics.ListAPIView):
#     # sql = """select * from pgr_dijkstra(
#     #         'select gid as id, source, target, cost from ways',
#     #         1,
#     #         346,
#     #         directed := FALSE
#     #         );"""
#     # queryset = Way.objects.raw(sql)
#     serializer_class = WaySerializer
import psycopg2
@api_view(["GET"])
@permission_classes((AllowAny,))
def ListWays(request):
    # sql = """select gid from pgr_dijkstra(
    #     'select gid as id, source, target, cost from ways',
    #     1,
    #     346,
    #     directed := FALSE
    #     );"""
    # return Way.objects.raw("select * from ways;")
    with connections['default'].cursor() as cursor:
        cursor.execute("""select * from pgr_dijkstra(
        'select gid as id, source, target, cost from ways',
        1,
        346,
        directed := FALSE
        );""")
        row = cursor.fetchall()
    # query = Dijkstra.objects.filter(seq__in=row)
    print("QUERY: ", row)
    return Response(row)





# class CreateWaysDijkstra(generics.ListCreateAPIView):
#     queryset = Way.objects.all()
#     serializer_class = WaySerializer
#
#     # def perform_create(self, serializer):
#     #     address = serializer.initial_data('address')
#     #     g = geocoder.google(address)
#     #     latitude = g.latlng[0]
#     #     longitude = g.latlng[1]
#     #     pnt = 'POINT(' + str(longitude) + ' ' + str(latitude) + '}'
#     #     serializer.save(location=pnt)
#
#     def get_queryset(self):
#         # Way.objects.raw('select * from pgr_dijkstra('select gid as id, source, target, cost from ways', 1, 346, directed := FALSE)')
#         qs = super().get_queryset()
#         sql = """
#                     SELECT *, v.lon::double precision, v.lat::double precision
#                     FROM
#                         pgr_dijkstra(
#                             'SELECT {id} as id,
#                                     {source} as source,
#                                     {target} as target,
#                                     {cost} as cost,
#                                     {reverse_cost} as reverse_cost
#                              FROM {edge_table}',
#                             %s,
#                             %s,
#                             {directed}) as r,
#                         {edge_table}_vertices_pgr as v
#                     WHERE r.node=v.id
#                     ORDER BY r.seq;
#                     """.format(
#             edge_table='ways',
#             id=qs.,
#             source=self._meta_data['source'],
#             target=self._meta_data['target'],
#             cost=self._meta_data['cost'],
#             reverse_cost=self._meta_data['reverse_cost'],
#             directed='TRUE'
#             if self._meta_data['directed']
#             else 'FALSE')

        # qs = super().get_queryset()
        # latitude = self.request.query_params.get('lat', None)
        # longitude = self.request.query_params.get('lng', None)
        #
        # if latitude and longitude:
        #     pnt = GEOSGeometry('POINT(' + str(longitude) + ' ' + str(latitude) + '}', srid=4326)


# @api_view(["POST"])
# @permission_classes((IsAuthenticated,))
# def dijkstra(request):
#     # serialized = GroupSerializer(data=request.data, context={"request": request})
#     # # if serialized.is_valid():
#     # s = serialized.save()
#     # return Response(ShowingGroupSerializer(s, context={'request':request}).data, status=HTTP_200_OK)
#     # return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)
#     with connection.cursor() as cursor:
#         sql = """select * from pgr_dijkstra(
#             'select gid as id, source, target, cost from ways',
#             1,
#             346,
#             directed := FALSE
#             );"""
#         cursor.execute(sql)
#         row = cursor.fetchone()
#         all_count, yes_count = row
#
#         # if request.method == 'GET':
#         #     return Response(Way.objects.raw(sql), status=200)