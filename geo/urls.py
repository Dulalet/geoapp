from django.urls import path
from .views import *


urlpatterns = [
    path('buildings/', ListBuilding.as_view(), name="buildings"),
    path('buildings/create/', CreateBuilding.as_view(), name="buildings-create"),
    path('buildings/<int:pk>', UpdateBuilding.as_view(), name="buildings-update"),
    path('buildings/<int:pk>/delete', DeleteBuilding.as_view(), name="buildings-delete"),

    path('busstops/', ListBusStop.as_view(), name="busstops"),
    path('busstops/create/', CreateBusStop.as_view(), name="busstops-create"),
    path('busstops/<int:pk>', UpdateBusStop.as_view(), name="busstops-update"),
    path('busstops/<int:pk>/delete', DeleteBusStop.as_view(), name="busstops-delete"),

    path('redlines/', ListRedLine.as_view(), name="redlines"),
    path('redlines/create/', CreateRedLine.as_view(), name="redlines-create"),
    path('redlines/<int:pk>', UpdateRedLine.as_view(), name="redlines-update"),
    path('redlines/<int:pk>/delete', DeleteRedLine.as_view(), name="redlines-delete"),

    path('streets/', ListStreet.as_view(), name="streets"),
    path('streets/create/', CreateStreet.as_view(), name="streets-create"),
    path('streets/<int:pk>', UpdateStreet.as_view(), name="streets-update"),
    path('streets/<int:pk>/delete', DeleteStreet.as_view(), name="streets-delete"),
]