# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.contrib.gis.db import models
#
#
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'
#
#
# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)
#
#
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user'
#
#
# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)
#
#
# class BuildingsProject(models.Model):
#     ogc_fid = models.AutoField(primary_key=True)
#     id = models.IntegerField(blank=True, null=True)
#     floor = models.CharField(max_length=100, blank=True, null=True)
#     status = models.CharField(max_length=100, blank=True, null=True)
#     data_in = models.DateField(blank=True, null=True)
#     function = models.CharField(max_length=100, blank=True, null=True)
#     id_style1 = models.IntegerField(blank=True, null=True)
#     build_area = models.FloatField(blank=True, null=True)
#     use_area = models.FloatField(blank=True, null=True)
#     number_apa = models.FloatField(blank=True, null=True)
#     population = models.FloatField(blank=True, null=True)
#     seats = models.FloatField(blank=True, null=True)
#     seats_cars = models.FloatField(blank=True, null=True)
#     shape_leng = models.FloatField(blank=True, null=True)
#     shape_le_1 = models.FloatField(blank=True, null=True)
#     shape_area = models.FloatField(blank=True, null=True)
#     wkb_geometry = models.GeometryField(srid=3857, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'buildings_project'
#
#
# class BusStopsProject1(models.Model):
#     ogc_fid = models.AutoField(primary_key=True)
#     stationnam = models.CharField(max_length=100, blank=True, null=True)
#     platformx = models.CharField(max_length=100, blank=True, null=True)
#     platformy = models.CharField(max_length=100, blank=True, null=True)
#     wkb_geometry = models.PointField(srid=3857, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'bus_stops_project1'
#
#
# class Configuration(models.Model):
#     tag_id = models.IntegerField(unique=True, blank=True, null=True)
#     tag_key = models.TextField(blank=True, null=True)
#     tag_value = models.TextField(blank=True, null=True)
#     priority = models.FloatField(blank=True, null=True)
#     maxspeed = models.FloatField(blank=True, null=True)
#     maxspeed_forward = models.FloatField(blank=True, null=True)
#     maxspeed_backward = models.FloatField(blank=True, null=True)
#     force = models.CharField(max_length=1, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'configuration'
#
#
# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'
#
#
# class Input(models.Model):
#     ogc_fid = models.AutoField(primary_key=True)
#     id = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=100, blank=True, null=True)
#     type = models.CharField(max_length=100, blank=True, null=True)
#     old_type = models.CharField(max_length=100, blank=True, null=True)
#     abreviatur = models.CharField(max_length=100, blank=True, null=True)
#     shape_leng = models.FloatField(blank=True, null=True)
#     shape_le_1 = models.FloatField(blank=True, null=True)
#     geom = models.LineStringField(srid=3857, blank=True, null=True)
#     source = models.IntegerField(blank=True, null=True)
#     target = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'input'
#
#
# class InputVerticesPgr(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     cnt = models.IntegerField(blank=True, null=True)
#     chk = models.IntegerField(blank=True, null=True)
#     ein = models.IntegerField(blank=True, null=True)
#     eout = models.IntegerField(blank=True, null=True)
#     the_geom = models.PointField(srid=3857, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'input_vertices_pgr'
#
#
# class Layer(models.Model):
#     topology = models.ForeignKey('Topology', models.DO_NOTHING, primary_key=True)
#     layer_id = models.IntegerField()
#     schema_name = models.CharField(max_length=-1)
#     table_name = models.CharField(max_length=-1)
#     feature_column = models.CharField(max_length=-1)
#     feature_type = models.IntegerField()
#     level = models.IntegerField()
#     child_id = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'layer'
#         unique_together = (('topology', 'layer_id'), ('schema_name', 'table_name', 'feature_column'),)
#
#
# class Pointsofinterest(models.Model):
#     pid = models.BigAutoField(primary_key=True)
#     osm_id = models.BigIntegerField(unique=True, blank=True, null=True)
#     vertex_id = models.BigIntegerField(blank=True, null=True)
#     edge_id = models.BigIntegerField(blank=True, null=True)
#     side = models.CharField(max_length=1, blank=True, null=True)
#     fraction = models.FloatField(blank=True, null=True)
#     length_m = models.FloatField(blank=True, null=True)
#     tag_name = models.TextField(blank=True, null=True)
#     tag_value = models.TextField(blank=True, null=True)
#     name = models.TextField(blank=True, null=True)
#     the_geom = models.PointField(blank=True, null=True)
#     new_geom = models.PointField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'pointsofinterest'
#
#
# class RedLinesProject(models.Model):
#     ogc_fid = models.AutoField(primary_key=True)
#     id_style = models.CharField(max_length=100, blank=True, null=True)
#     id_style1 = models.IntegerField(blank=True, null=True)
#     shape_leng = models.FloatField(blank=True, null=True)
#     shape_le_1 = models.FloatField(blank=True, null=True)
#     wkb_geometry = models.LineStringField(srid=3857, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'red_lines_project'
#
#
# class StreetsProject(models.Model):
#     ogc_fid = models.AutoField(primary_key=True)
#     id = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=100, blank=True, null=True)
#     type = models.CharField(max_length=100, blank=True, null=True)
#     old_type = models.CharField(max_length=100, blank=True, null=True)
#     abreviatur = models.CharField(max_length=100, blank=True, null=True)
#     shape_leng = models.FloatField(blank=True, null=True)
#     shape_le_1 = models.FloatField(blank=True, null=True)
#     source = models.IntegerField(blank=True, null=True)
#     target = models.IntegerField(blank=True, null=True)
#     geom = models.LineStringField(srid=3857, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'streets_project'
#
#
# class StreetsProjectVerticesPgr(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     cnt = models.IntegerField(blank=True, null=True)
#     chk = models.IntegerField(blank=True, null=True)
#     ein = models.IntegerField(blank=True, null=True)
#     eout = models.IntegerField(blank=True, null=True)
#     the_geom = models.PointField(srid=3857, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'streets_project_vertices_pgr'
#
#
# class Topology(models.Model):
#     name = models.CharField(unique=True, max_length=-1)
#     srid = models.IntegerField()
#     precision = models.FloatField()
#     hasz = models.BooleanField()
#
#     class Meta:
#         managed = False
#         db_table = 'topology'
#
#
# class Ways(models.Model):
#     gid = models.BigAutoField(primary_key=True)
#     osm_id = models.BigIntegerField(blank=True, null=True)
#     tag = models.ForeignKey(Configuration, models.DO_NOTHING, blank=True, null=True)
#     length = models.FloatField(blank=True, null=True)
#     length_m = models.FloatField(blank=True, null=True)
#     name = models.TextField(blank=True, null=True)
#     source = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, db_column='source', blank=True, null=True)
#     target = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, db_column='target', blank=True, null=True)
#     source_osm = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, db_column='source_osm', blank=True, null=True)
#     target_osm = models.ForeignKey('WaysVerticesPgr', models.DO_NOTHING, db_column='target_osm', blank=True, null=True)
#     cost = models.FloatField(blank=True, null=True)
#     reverse_cost = models.FloatField(blank=True, null=True)
#     cost_s = models.FloatField(blank=True, null=True)
#     reverse_cost_s = models.FloatField(blank=True, null=True)
#     rule = models.TextField(blank=True, null=True)
#     one_way = models.IntegerField(blank=True, null=True)
#     oneway = models.TextField(blank=True, null=True)
#     x1 = models.FloatField(blank=True, null=True)
#     y1 = models.FloatField(blank=True, null=True)
#     x2 = models.FloatField(blank=True, null=True)
#     y2 = models.FloatField(blank=True, null=True)
#     maxspeed_forward = models.FloatField(blank=True, null=True)
#     maxspeed_backward = models.FloatField(blank=True, null=True)
#     priority = models.FloatField(blank=True, null=True)
#     the_geom = models.LineStringField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'ways'
#
#
# class WaysVerticesPgr(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     osm_id = models.BigIntegerField(unique=True, blank=True, null=True)
#     eout = models.IntegerField(blank=True, null=True)
#     lon = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
#     lat = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
#     cnt = models.IntegerField(blank=True, null=True)
#     chk = models.IntegerField(blank=True, null=True)
#     ein = models.IntegerField(blank=True, null=True)
#     the_geom = models.PointField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'ways_vertices_pgr'
