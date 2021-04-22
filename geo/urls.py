from django.urls import path
from .views import *


urlpatterns = [
    # api для расчета маршрутов с учтом барьеров
    path('path/', ListWays, name="path"),

    # api для добавления слоя
    path('addLayer/', addLayer, name='addLayer'),

    # api для расчета объектов в заданном радиусе
    path('countObjects/', countObjects, name='countObjects'),

    # api для расставления объектов (КПП и случайные точки) в буферной зоне
    path('buffer/', buffer, name='buffer'),

    # api для поиска ближайших объектов
    path('nearest/', showNearest, name='nearest'),

    # api для создания буферных зон с учетом контуров зданий
    path('bufferize/', get_buffer_zone, name='bufferize'),

    # api для расчета зон видимости
    path('visibility/', get_visibility_zones),

    # api для импорта медиа
    path('importMedia/', import_media),

    # CRUD для buildings
    path('buildings/', ListBuilding.as_view(), name="buildings"),
    path('buildings/create/', CreateBuilding.as_view(), name="buildings-create"),
    # path('buildings/<int:pk>/', UpdateBuilding.as_view(), name="buildings-update"),
    path('buildings/update/', UpdateBuilding, name="buildings-update"),
    path('buildings/delete/', DeleteBuilding, name="buildings-delete"),

    # CRUD для busstops
    path('busstops/', ListBusStop.as_view(), name="busstops"),
    path('busstops/create/', CreateBusStop.as_view(), name="busstops-create"),
    path('busstops/update/', UpdateBusStop, name="busstops-update"),
    path('busstops/delete/', DeleteBusStop, name="busstops-delete"),

    # CRUD для redlines
    path('redlines/', ListRedLine.as_view(), name="redlines"),
    path('redlines/create/', CreateRedLine.as_view(), name="redlines-create"),
    path('redlines/update/', UpdateRedLine, name="redlines-update"),
    path('redlines/delete/', DeleteRedLine, name="redlines-delete"),

    # CRUD для streets
    path('streets/', ListStreet.as_view(), name="streets"),
    path('streets/create/', CreateStreet.as_view(), name="streets-create"),
    path('streets/update/', UpdateStreet, name="streets-update"),
    path('streets/delete/', DeleteStreet, name="streets-delete"),

    # CRUD для heatmap
    path('heatmap/', ListHeatmap.as_view(), name="heatmap"),
    path('heatmap/create/', CreateHeatmap.as_view(), name="heatmap-create"),
    path('heatmap/<int:pk>/', UpdateHeatmap.as_view(), name="heatmap-update"),
    path('heatmap/<int:pk>/delete/', DeleteHeatmap.as_view(), name="heatmap-delete"),
]