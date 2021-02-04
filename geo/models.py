from django.contrib.gis.db import models


class Building(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    id = models.IntegerField(blank=True, null=True)
    floor = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    data_in = models.DateField(blank=True, null=True)
    function = models.CharField(max_length=100, blank=True, null=True)
    id_style1 = models.IntegerField(blank=True, null=True)
    build_area = models.FloatField(blank=True, null=True)
    use_area = models.FloatField(blank=True, null=True)
    number_apa = models.FloatField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    seats = models.FloatField(blank=True, null=True)
    seats_cars = models.FloatField(blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_le_1 = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    wkb_geometry = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        db_table = 'buildings_project'


class BusStop(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    stationnam = models.CharField(max_length=100, blank=True, null=True)
    platformx = models.CharField(max_length=100, blank=True, null=True)
    platformy = models.CharField(max_length=100, blank=True, null=True)
    wkb_geometry = models.PointField(srid=3857, blank=True, null=True)

    class Meta:
        db_table = 'bus_stops_project1'


class RedLine(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    id_style = models.CharField(max_length=100, blank=True, null=True)
    id_style1 = models.IntegerField(blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_le_1 = models.FloatField(blank=True, null=True)
    wkb_geometry = models.LineStringField(srid=3857, blank=True, null=True)

    class Meta:
        db_table = 'red_lines_project'


class Street(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    old_type = models.CharField(max_length=100, blank=True, null=True)
    abreviatur = models.CharField(max_length=100, blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_le_1 = models.FloatField(blank=True, null=True)
    wkb_geometry = models.GeometryField(srid=3857, blank=True, null=True)

    class Meta:
        db_table = 'streets_project'
