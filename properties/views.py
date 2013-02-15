import json
import time

from django.http import HttpResponse
from django.contrib.gis.geos import Point

from pygeocoder import Geocoder, GeocoderError
from models import ExpUse


def get_properties(request):
    # Return GeoJSON for all Expiring User get_properties

    expuse = ExpUse.objects.filter(geometry__isnull=False)

    features = []
    for prop in expuse:

        geojson_prop = dict(
            name = prop.property_name_text.title(), 
            hudid = prop.hudid,
            aka = prop.aka_title,
            address = prop.address,
            total = prop.property_total_unit_count,
            elderly = prop.units_elderly_c,
            br0 = prop.units_0br_c,
            br1 = prop.units_1br_c,
            br2 = prop.units_2br_c,
            br3 = prop.units_3br_c,
            br4m = prop.units_4mbr_c,
            assisted = prop.units_assisted,
            atrisk2015 = prop.units_at_risk_num_2015, 
            atrisk2020 = prop.units_at_risk_num_2020, 
            atrisk2025 = prop.units_at_risk_num_2025, 
        )
        if request.user.is_staff:
            geojson_prop['admin_url'] = prop.get_admin_url()
        geojson_geom = json.loads(prop.geometry.geojson)
        geojson_feat = dict(type='Feature', geometry=geojson_geom, properties=geojson_prop)
        features.append(geojson_feat)

    response = dict(type='FeatureCollection', features=features)

    return HttpResponse(json.dumps(response), mimetype='application/json')


def geocode_property(obj):

    if obj.geocoded is False:

        attempts = 0
        success = False

        while success != True and attempts < 3:
            try:
                result = Geocoder.geocode(obj.address)
                attempts += 1

                if result.valid_address:
                    obj.lat = result[0].coordinates[0]
                    obj.lon = result[0].coordinates[1]
                    obj.geometry = Point(obj.lon, obj.lat)
                    obj.geocoded_address = str(result)
                    obj.geocoded_type = result.raw[0]['geometry']['location_type']
                    obj.geocoded = True

                # no geocoding error
                success = True

            except GeocoderError, e:
                if 'OVER_QUERY_LIMIT' in e:
                    time.sleep(2)
                    # retry
                    continue
                else:
                    # not really true, but stop trying
                    # not sure what happened
                    success = True 
                    break

    return obj


