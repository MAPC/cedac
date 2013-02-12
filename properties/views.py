import json

from django.http import HttpResponse
from models import ExpUse


def get_properties(request):
    # Return GeoJSON for all Expiring User get_properties

    expuse = ExpUse.objects.all()

    features = []
    for prop in expuse:

        geojson_prop = dict(
            name = prop.property_name_text.title(), 
            hudid = prop.hudid,
            aka = prop.aka_title(),
            address = prop.address(),
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
        geojson_geom = json.loads(prop.geometry.geojson)
        geojson_feat = dict(type='Feature', geometry=geojson_geom, properties=geojson_prop)
        features.append(geojson_feat)

    response = dict(type='FeatureCollection', features=features)

    return HttpResponse(json.dumps(response), mimetype='application/json')


