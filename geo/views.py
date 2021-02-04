# from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from geo.serializers import UserSerializer, GroupSerializer, BuildingSerializer, \
    BusStopSerializer, RedLineSerializer, StreetSerializer
from geo.models import Building, BusStop, RedLine, Street


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


