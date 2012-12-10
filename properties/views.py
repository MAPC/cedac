import json

from django.http import HttpResponse
from models import ExpUse


def get_properties(request):
    # Return GeoJSON for all Expiring User get_properties

    expuse = ExpUse.objects.all()

    features = []
    for prop in expuse:

        address = '%s, %s, MA %s' % (prop.address_line1_text.title(), prop.city_name_text.title(), prop.zip_code)

        geojson_prop = dict(name=prop.property_name_text.title(), atrisk2015=prop.units_at_risk_num2015, address=address)
        geojson_geom = json.loads(prop.geometry.geojson)
        geojson_feat = dict(type='Feature', geometry=geojson_geom, properties=geojson_prop)
        features.append(geojson_feat)

    response = dict(type='FeatureCollection', features=features)

    return HttpResponse(json.dumps(response), mimetype='application/json')


