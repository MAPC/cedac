from django.contrib.gis import admin
from models import ExpUse


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7915039
admin.GeoModelAdmin.default_lat = 5216500 
admin.GeoModelAdmin.default_zoom = 11


class ExpUseAdmin(admin.OSMGeoAdmin):
    fieldsets = [
        (None, {
            'fields': ['propertyid', 'hudid', 'property_name_text', 'project_aka', ]
        }),
        ('Datafields', {
            'fields': ['units_0br_c', 'units_1br_c', 'units_2br_c', 'units_3br_c', 'units_4mbr_c', 'units_elderly_c', 'units_assisted', 'units_at_risk_num_2015', 'units_at_risk_num_2020', 'units_at_risk_num_2025', ]
        }),
        ('Location', {
            'fields': ['address_line1_text', 'zip_code', 'city_name_text', 'geocoded', 'geocoded_address', 'geometry', ]
        }),
    ]    
    list_filter = ['city_name_text', 'geocoded',]
    list_display = ('propertyid', 'hudid', 'property_name_text', 'project_aka', 'geocoded',)
    search_fields = ['property_name_text', 'project_aka']
    readonly_fields = ('geocoded', 'geocoded_address',)
    ordering = ['propertyid']


admin.site.register(ExpUse, ExpUseAdmin)
