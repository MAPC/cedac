from django.contrib.gis import admin
from models import ExpUse


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7915039
admin.GeoModelAdmin.default_lat = 5216500 
admin.GeoModelAdmin.default_zoom = 11


admin.site.register(ExpUse, admin.OSMGeoAdmin)
