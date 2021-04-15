from django.urls import path
from .views import *


urlpatterns = [
    path('path/', ListWays, name="path"),
    path('addLayer/', addLayer, name='addLayer'),
    path('countObjects/', countObjects, name='countObjects'),
    path('buffer/', buffer, name='buffer'),
    path('nearest/', showNearest, name='nearest'),
    path('bufferize/', get_buffer_zone, name='bufferize'),
    path('visibility/', get_visibility_zones),

    path('buildings/', ListBuilding.as_view(), name="buildings"),
    path('buildings/create/', CreateBuilding.as_view(), name="buildings-create"),
    # path('buildings/<int:pk>/', UpdateBuilding.as_view(), name="buildings-update"),
    path('buildings/update/', UpdateBuilding, name="buildings-update"),
    path('buildings/delete/', DeleteBuilding, name="buildings-delete"),

    path('busstops/', ListBusStop.as_view(), name="busstops"),
    path('busstops/create/', CreateBusStop.as_view(), name="busstops-create"),
    path('busstops/update/', UpdateBusStop, name="busstops-update"),
    path('busstops/delete/', DeleteBusStop, name="busstops-delete"),

    path('redlines/', ListRedLine.as_view(), name="redlines"),
    path('redlines/create/', CreateRedLine.as_view(), name="redlines-create"),
    path('redlines/update/', UpdateRedLine, name="redlines-update"),
    path('redlines/delete/', DeleteRedLine, name="redlines-delete"),

    path('streets/', ListStreet.as_view(), name="streets"),
    path('streets/create/', CreateStreet.as_view(), name="streets-create"),
    path('streets/update/', UpdateStreet, name="streets-update"),
    path('streets/delete/', DeleteStreet, name="streets-delete"),

    path('heatmap/', ListHeatmap.as_view(), name="heatmap"),
    path('heatmap/create/', CreateHeatmap.as_view(), name="heatmap-create"),
    path('heatmap/<int:pk>/', UpdateHeatmap.as_view(), name="heatmap-update"),
    path('heatmap/<int:pk>/delete/', DeleteHeatmap.as_view(), name="heatmap-delete"),
]