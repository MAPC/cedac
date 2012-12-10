import json

from django.http import HttpResponse
from models import Category, Layer
from django.db.models import Min, Max


def get_categories():
    # Returns JSON category configuration

    categories = Category.objects.all()

    response = [ dict(title=category.title, slug=category.slug) for category in categories ]

    return response


def get_layers():
    # Returns JSON map layer configuration

    layers = Layer.objects.all()

    response = []

    for layer in layers:
        zindex = 20 + layer.map_order * 10
        wms_obj = dict(
            url=layer.wms_server.url, 
            layers=layer.wms_layers, 
            styles=layer.wms_styles, 
            format=layer.wms_format, 
            transparent=layer.wms_transparent,
            attribution=layer.wms_server.attribution,
        )
        layer_obj = dict(
            title=layer.title, 
            category=layer.category.slug, 
            visible=layer.visible, 
            zindex=zindex,
            wms=wms_obj,
        )
        response.append(layer_obj)

    return response


def get_app_config(request):
    # get JSON app config

    categories = get_categories()
    layers = get_layers()

    response = dict(categories=categories, layers=layers)

    return HttpResponse(json.dumps(response), mimetype='application/json')