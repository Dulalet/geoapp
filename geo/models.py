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


class WaysVerticesPgr(models.Model):
    id = models.BigAutoField(primary_key=True)
    osm_id = models.BigIntegerField(unique=True, blank=True, null=True)
    eout = models.IntegerField(blank=True, null=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    lat = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)
    chk = models.IntegerField(blank=True, null=True)
    ein = models.IntegerField(blank=True, null=True)
    the_geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ways_vertices_pgr'


class Way(models.Model):
    gid = models.BigAutoField(primary_key=True)
    osm_id = models.BigIntegerField(blank=True, null=True)
    # tag = models.ForeignKey(Configuration, models.DO_NOTHING, blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    length_m = models.FloatField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    source = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, related_name='sources', db_column='source', blank=True, null=True)
    target = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, related_name='targets', db_column='target', blank=True, null=True)
    source_osm = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, related_name='sources_osm', db_column='source_osm', blank=True, null=True)
    target_osm = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, related_name='targets_osm', db_column='target_osm', blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    reverse_cost = models.FloatField(blank=True, null=True)
    cost_s = models.FloatField(blank=True, null=True)
    reverse_cost_s = models.FloatField(blank=True, null=True)
    rule = models.TextField(blank=True, null=True)
    one_way = models.IntegerField(blank=True, null=True)
    oneway = models.TextField(blank=True, null=True)
    x1 = models.FloatField(blank=True, null=True)
    y1 = models.FloatField(blank=True, null=True)
    x2 = models.FloatField(blank=True, null=True)
    y2 = models.FloatField(blank=True, null=True)
    maxspeed_forward = models.FloatField(blank=True, null=True)
    maxspeed_backward = models.FloatField(blank=True, null=True)
    priority = models.FloatField(blank=True, null=True)
    the_geom = models.LineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ways'

    def __str__(self):
        return self.name
