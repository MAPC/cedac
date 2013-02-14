
from django.contrib.gis import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.translation import ugettext as _

import csv

from models import ExpUse
from views import geocode_property


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7915039
admin.GeoModelAdmin.default_lat = 5216500 
admin.GeoModelAdmin.default_zoom = 11

def geocode_properties(modeladmin, request, queryset):
    """
    Geocode selected objects against Google
    """

    if not request.user.is_staff:
        raise PermissionDenied
    
    for obj in queryset:
        obj = geocode_property(obj)
        obj.save()

geocode_properties.short_description = _('Geocode selected %(verbose_name_plural)s')

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """

    if not request.user.is_staff:
        raise PermissionDenied

    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    
    field_names = [field.name for field in opts.fields]
    
    # Write a first row with header information
    writer.writerow(field_names)
    
    # Write data rows
    for obj in queryset:
        try:
            writer.writerow([getattr(obj, field) for field in field_names])
        except UnicodeEncodeError:
            print 'Could not export data row.'
    return response

export_as_csv.short_description = _('Export selected %(verbose_name_plural)s as CSV file')

class ExpUseAdmin(admin.OSMGeoAdmin):
    fieldsets = [
        (None, {
            'fields': ['propertyid', 'hudid', 'property_name_text', 'project_aka', ]
        }),
        ('Datafields', {
            'fields': ['units_0br_c', 'units_1br_c', 'units_2br_c', 'units_3br_c', 'units_4mbr_c', 'units_elderly_c', 'units_assisted', 'units_at_risk_num_2015', 'units_at_risk_num_2020', 'units_at_risk_num_2025', ]
        }),
        ('Location', {
            'fields': ['address_line1_text', 'zip_code', 'city_name_text', 'geocoded', 'geocoded_address', 'geocoded_type', 'geometry', ]
        }),
    ]    
    list_filter = ['city_name_text', 'geocoded', 'geocoded_type']
    list_display = ('propertyid', 'property_name_text', 'address_line1_text', 'zip_code', 'city_name_text', 'geocoded',)
    list_editable = ['property_name_text', 'address_line1_text', 'zip_code', 'city_name_text',]
    search_fields = ['property_name_text', 'project_aka']
    readonly_fields = ('geocoded', 'geocoded_address', )
    ordering = ['propertyid']
    actions = [geocode_properties, export_as_csv]


admin.site.register(ExpUse, ExpUseAdmin)
