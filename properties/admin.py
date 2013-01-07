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
            'fields': ['units_0br_c', 'units_1br_c', 'units_2br_c', 'units_3br_c', 'units_4br_c', 'units_5br_c', 'units_elderly_c', 'units_nonelderly_c', 'units_assisted', 'orig_units_assisted_c', 'isatrisk2015', 'units_at_risk_num2015', 'units_retained_c_2015', 'isatrisk2020', 'units_at_risk_num2020', 'units_retained_c_2020', 'isatrisk2025', 'units_at_risk_num2025', 'units_retained_c_2025', ]
        }),
        ('Location', {
            'fields': ['address_line1_text', 'zip_code', 'city_name_text', 'geometry', ]
        }),
    ]    
    list_filter = ['city_name_text', ]
    list_display = ('propertyid', 'hudid', 'property_name_text', 'project_aka',)
    search_fields = ['property_name_text', 'project_aka']
    ordering = ['id']


admin.site.register(ExpUse, ExpUseAdmin)
