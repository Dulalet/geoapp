import psycopg2
from django.contrib.auth.models import User, Group
from django.db import connections
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from geo.models import Building, BusStop, RedLine, Street
from geo.serializers import UserSerializer, GroupSerializer, BuildingSerializer, \
    BusStopSerializer, RedLineSerializer, StreetSerializer


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


@api_view(["GET"])
@permission_classes((AllowAny,))
def ListWays(request):
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
    print("QUERY: ", row)
    return Response(row)


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