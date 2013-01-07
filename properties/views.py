import json

from django.http import HttpResponse
from models import ExpUse


def get_properties(request):
    # Return GeoJSON for all Expiring User get_properties

    expuse = ExpUse.objects.all()

    features = []
    for prop in expuse:

        address = '%s, %s, MA %s' % (prop.address_line1_text.title(), prop.city_name_text.title(), prop.zip_code)

        geojson_prop = dict(
            name = prop.property_name_text.title(), 
            hudid = prop.hudid,
            aka = prop.aka_title(),
            address = address,
            nonelderly = prop.units_nonelderly_c,
            elderly = prop.units_elderly_c,
            br0 = prop.units_0br_c,
            br1 = prop.units_1br_c,
            br2 = prop.units_2br_c,
            br3 = prop.units_3br_c,
            br4 = prop.units_4br_c,
            br5 = prop.units_5br_c,
            assisted = prop.units_assisted,
            orig_assisted = prop.orig_units_assisted_c,
            isatrisk2015 = prop.isatrisk2015,
            atrisk2015 = prop.units_at_risk_num2015, 
            retained2015 = prop.units_retained_c_2015,
        )
        geojson_geom = json.loads(prop.geometry.geojson)
        geojson_feat = dict(type='Feature', geometry=geojson_geom, properties=geojson_prop)
        features.append(geojson_feat)

    response = dict(type='FeatureCollection', features=features)

    return HttpResponse(json.dumps(response), mimetype='application/json')


