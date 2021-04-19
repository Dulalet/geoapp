import os
from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED

from geo.buffer import buffer_generate
from geo.forms import *
from geo.importshp import importLayer, gdf2layer, import_from_db, normalize_gdf
from geo.nearestObjects import nearestPoints
from geo.objectsInPolygon import numObjects
from geo.serializers import *
from geoapp.settings import MEDIA_URL
from geoapp.tasks import remove_barriers


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
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class ListBuilding(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


@api_view(["PUT"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def UpdateBuilding(request):
    obj = get_object_or_404(Building, uuid=request.data['uuid'])
    form = BuildingForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
    return Response(BuildingSerializer(obj).data)


@api_view(["DELETE"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def DeleteBuilding(request):
    obj = get_object_or_404(Building, uuid=request.data['uuid'])

    if request.method == 'DELETE':
        obj.delete()
    return Response('deleted', HTTP_202_ACCEPTED)


class CreateBusStop(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


class ListBusStop(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


@api_view(["PUT"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def UpdateBusStop(request):
    obj = get_object_or_404(BusStop, uuid=request.data['uuid'])
    form = BusStopForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
    return Response(BusStopSerializer(obj).data)


@api_view(["DELETE"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def DeleteBusStop(request):
    obj = get_object_or_404(BusStop, uuid=request.data['uuid'])

    if request.method == 'DELETE':
        obj.delete()
    return Response('deleted', HTTP_202_ACCEPTED)


class CreateRedLine(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = RedLine.objects.all()
    serializer_class = RedLineSerializer


class ListRedLine(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = RedLine.objects.all()
    serializer_class = RedLineSerializer


@api_view(["PUT"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def UpdateRedLine(request):
    obj = get_object_or_404(RedLine, uuid=request.data['uuid'])
    form = RedLineForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
    return Response(RedLineSerializer(obj).data)


@api_view(["DELETE"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def DeleteRedLine(request):
    obj = get_object_or_404(RedLine, uuid=request.data['uuid'])

    if request.method == 'DELETE':
        obj.delete()
    return Response('deleted', HTTP_202_ACCEPTED)


class CreateStreet(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class ListStreet(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


@api_view(["PUT"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def UpdateStreet(request):
    obj = get_object_or_404(Street, uuid=request.data['uuid'])
    form = StreetForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
    return Response(StreetSerializer(obj).data)


@api_view(["DELETE"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def DeleteStreet(request):
    obj = get_object_or_404(Street, uuid=request.data['uuid'])

    if request.method == 'DELETE':
        obj.delete()
    return Response('deleted', HTTP_202_ACCEPTED)


class CreateHeatmap(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


class ListHeatmap(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


class UpdateHeatmap(generics.RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


class DeleteHeatmap(generics.DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    queryset = Heatmap.objects.all()
    serializer_class = HeatmapSerializer


@api_view(["GET"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def get_layer(request):
    if request.user.is_superuser:
        queryset = Layer.objects.all()
        # print(queryset)
    else:
        from django.db.models import Q
        queryset = Layer.objects.filter(Q(is_general=True) | Q(user=request.user.id))
    return Response(LayerSerializer(queryset, many=True).data)


# class UpdateLayer(generics.RetrieveUpdateAPIView):
#     queryset = Layer.objects.all()
#     serializer_class = LayerSerializer


@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def ListWays(request):
    vertexSerializer = VertexSerializer(data=request.data)
    distance = 0
    if vertexSerializer.is_valid():
        distance += vertexSerializer.data['closest_source']['distance']
        distance += vertexSerializer.data['closest_destination']['distance']
        if vertexSerializer.data['geometry'] is not None:
            conn = connections['default']
            conn.ensure_connection()
            with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""UPDATE ways
                                SET barrier=TRUE
                                FROM (
                                         SELECT streets.gid AS gid, streets.the_geom AS geometry
                                         FROM ways streets
                                         WHERE ST_Intersects(streets.the_geom, '{geom}'::geography) = TRUE
                                ) t
                                WHERE ways.gid = t.gid;""".format(geom=vertexSerializer.data['geometry']))
        conn = connections['default']
        conn.ensure_connection()
        with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM pgr_dijkstra(
                'select gid as id, source, target, length_m as cost from ways where ways.barrier=false',
                {node_from},
                {node_to},
                directed := FALSE
                );""".format(node_from=vertexSerializer.data['closest_source']['node'],
                             node_to=vertexSerializer.data['closest_destination']['node']))
            row = cursor.fetchall()
        if row:
            distance += row[-1]['agg_cost']
        serialized = DijkstraSerializer(row, many=True)
        result = {'total_distance': distance, 'source_point': vertexSerializer.data['source_point'],
                  'destination_point': vertexSerializer.data['destination_point'], 'path': serialized.data}

        print(vertexSerializer.validated_data['barrier_time'])
        remove_barriers.apply_async(eta=vertexSerializer.validated_data['barrier_time'])
        return Response(result)


@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
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
            layer = gdf2layer(name=name, filepath=uploaded_file_url, user=request.user)
            serialized_layer = LayerSerializer(layer)
        except ImportError:
            return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        finally:
            fs.delete(file.name)
        return Response(serialized_layer.data)
    return Response('Error', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def countObjects(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        if serialized.validated_data['from_file']:
            media = os.getcwd()
            fs = FileSystemStorage(location=media + '/layer_files')
            file = serialized.validated_data['file']
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.path(filename)
            serialized.validated_data.pop('file')
            try:
                gdf = importLayer(uploaded_file_url)
                objectsNum, objects = numObjects(pointX, pointY, radius, gdf, serialized.validated_data['from_file'])
            except ImportError:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
            finally:
                fs.delete(file.name)
        else:
            try:
                gdf = import_from_db(serialized.validated_data['id'])
                objectsNum, objects = numObjects(pointX, pointY, radius, gdf, serialized.validated_data['from_file'])
            except:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)

        return Response({'number of objects': str(objectsNum), 'objects': objects})
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def buffer(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        if serialized.validated_data['from_file']:
            media = os.getcwd()
            fs = FileSystemStorage(location=media + '/layer_files')
            file = serialized.validated_data['file']
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.path(filename)
            serialized.validated_data.pop('file')
            try:
                gdf = importLayer(uploaded_file_url)
                kpp_points, randomPoints = buffer_generate(pointX, pointY, radius, gdf, serialized.validated_data['from_file'])
            except ImportError:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
            finally:
                fs.delete(file.name)
        else:
            try:
                gdf = import_from_db(serialized.validated_data['id'])
                kpp_points, randomPoints = buffer_generate(pointX, pointY, radius, gdf, serialized.validated_data['from_file'])
            except:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        return Response({'KPP': kpp_points.to_json(),
                         'Random Points': randomPoints})
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def showNearest(request):
    serialized = PointRadiusSerializer(data=request.data)
    if serialized.is_valid():
        pointX = serialized.validated_data['pointX']
        pointY = serialized.validated_data['pointY']
        radius = serialized.validated_data['radius']
        if serialized.validated_data['from_file']:
            media = os.getcwd()
            fs = FileSystemStorage(location=media + '/layer_files')
            file = serialized.validated_data['file']
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.path(filename)
            serialized.validated_data.pop('file')
            try:
                gdf = importLayer(uploaded_file_url)
                pointsDict = nearestPoints(pointX, pointY, radius, gdf, serialized.validated_data['from_file'])
            except ImportError:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
            finally:
                fs.delete(file.name)
        else:
            try:
                gdf = import_from_db(serialized.validated_data['id'])
                pointsDict = nearestPoints(pointX, pointY, radius, gdf, serialized.validated_data['from_file'])
            except:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        return Response(json.dumps(pointsDict))
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
@permission_classes((IsAuthenticated,))
def get_buffer_zone(request):
    serialized = BufferZoneSerializer(data=request.data)
    if serialized.is_valid():
        if serialized.validated_data['from_file']:
            media = os.getcwd()
            fs = FileSystemStorage(location=media + '/layer_files')
            file = serialized.validated_data['file']
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.path(filename)
            serialized.validated_data.pop('file')
            try:
                gdf = importLayer(uploaded_file_url)
                gdf = gdf.buffer(serialized.validated_data['radius'])
            except:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
            finally:
                fs.delete(file.name)
        else:
            try:
                gdf = import_from_db(serialized.validated_data['id'])
                gdf = normalize_gdf(gdf)
                gdf = gdf.buffer(serialized.validated_data['radius'])
            except:
                return Response('Error, invalid input', HTTP_400_BAD_REQUEST)
        return Response(gdf.geometry.to_json())
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


from geo.visibility_zones import get_visibility


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
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
        # second_file = serialized.validated_data['second_file']
        media = os.getcwd()
        fs = FileSystemStorage(location=media + '/visibility_files')
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.path(filename)
        serialized.validated_data.pop('file')
        path = Path(uploaded_file_url)
        cmd = f"gdal_viewshed -md {observer_radius} -ox {observer_x} -oy {observer_y} -oz {observer_height} {uploaded_file_url} {path.parent}/out1.tiff"
        file_path = str(path.parent) + '/out1.tiff'
        os.system(cmd)
        result = {}
        if second_observer_x and second_observer_y:
            print('test')
            cmd = f"gdal_viewshed -md {second_observer_radius} -ox {second_observer_x} -oy {second_observer_y} -oz {second_observer_height} -vv 200 {uploaded_file_url} {path.parent}/out2.tiff "
            os.system(cmd)
            second_file_path = str(path.parent) + '/out2.tiff'
            # try:
            vis_first, vis_second, vis_both = get_visibility(file_path, second_file_path)
            # except Exception as e:
            #     print(e)
            # finally:
            fs.delete(file.name)
            # fs.delete(second_file.name)
            result['vis_zone_first'] = str(vis_first)
            result['vis_zone_second'] = str(vis_second)
            result['vis_zone_mutual'] = str(vis_both)
        else:
            try:
                vis = get_visibility(file_path)
            except Exception as e:
                print(e)
            finally:
                fs.delete(file.name)
                result['vis_zone'] = str(vis)
        return Response(result)
    return Response('Error, invalid input', HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
# @permission_classes((AllowAny,))
def import_media(request):
    serialized = FileUploadSerializer(data=request.data)
    if serialized.is_valid():
        media = os.getcwd()
        fs = FileSystemStorage(location=media + MEDIA_URL)
        file = serialized.validated_data['file']
        filename = fs.save(file.name, file)
        uploaded_file_url = MEDIA_URL + filename
        serialized.validated_data.pop('file')
        return Response(uploaded_file_url, HTTP_202_ACCEPTED)

