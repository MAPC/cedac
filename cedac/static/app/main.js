window.cedac = window.cedac || {};


(function(){ 

    // initialize map
    function initMap( center, zoom ) {
        var map = L.map( "map", {
                minZoom: 8,
                maxZoom: 16
            } )
            .setView( center, zoom );

        // 2 hardcoded basemaps...
        var basemaps = [
            {
                title: "MAPC Basemap",
                category: "baselayerlist",
                layer: new L.MAPCTileLayer( "basemap" ),
                visible: true,
                zindex: 10
            },
            {
                title: "Bing Aerial",
                category: "baselayerlist",
                layer: new L.BingLayer("An8pfp-PjegjSInpD2JyXw5gMufAZBvZ_q3cbJb-kWiZ1H55gpJbxndbFHPsO_HN", "Aerial"),
                visible: false,
                zindex: 20,
            }
        ];
        this.initLayers( basemaps, map );

        return map;
    }

    // initialize category menu
    function initCategories ( categories ) {
        // category menu
        var html = _.template( "<div class='accordion-group'> \
            <div class='accordion-heading'> \
                <a class='accordion-toggle collapsed' data-toggle='collapse' href='#<%= slug %>'> \
                    <%= title %> \
                </a> \
            </div> \
            <div id='<%= slug %>' class='accordion-body collapse'> \
                <ul class='accordion-inner'></ul> \
            </div> \
        </div>" );
        
        _( categories ).forEach( function( category ) {
            $("#overlaylist").append( html( category ) );
        });
    }

    // initialize basemaps
    function initLayers( layers, map) {
        _( layers ).forEach( function( layer ) {

            // Leaflet Layer Object or new WMS layer
            if ( _.has(layer, 'layer') ) {
                var llLayer = layer.layer;
            }
            if ( _.has(layer, 'wms') ) {
                var llLayer = L.tileLayer.wms( layer.wms.url , {
                    layers: layer.wms.layers,
                    styles: layer.wms.styles,
                    format: layer.wms.format,
                    transparent: layer.wms.transparent,
                    attribution: layer.wms.attribution
                });
                llLayer.setOpacity(0.8);
                var legend = layer.wms.url + "?VERSION=1.1.0&REQUEST=GetLegendGraphic&FORMAT=image/png&LAYER=" + layer.wms.layers;
            }
            var legend = legend || "";

            var options = _.assign( layer , { 'layer': llLayer, 'legend': legend, 'map': map });
            var maplayer = new cedac.Layer( options );

            if ( layer.category === "baselayerlist" ) {
                cedac.baselayerlist.push( maplayer );
            }  
            if (layer.visible) maplayer.show();
        });
    }


    // expose functions
    cedac.initMap = initMap;
    cedac.initLayers = initLayers;
    cedac.initCategories = initCategories;

    // baselayers are radios
    cedac.baselayerlist = [];

    // BaseLayer module
    // TODO: maybe extend L.Class (http://leafletjs.com/reference.html#ilayer) instead?
    cedac.Layer = (function() {

        var Layer = function( options ) {
            this.layer = options.layer;
            this.title = options.title;
            this.category = options.category;
            this.category_slug = options.category.toLowerCase().replace(" ", "_");
            this.map = options.map;
            this.uuid = _.uniqueId( this.category_slug + "_" );
            this.legend = options.legend;
            this.zindex = options.zindex

            // add html template to layerlist
            if (this.category === "baselayerlist") {
                var html = _.template( "<li><label class='radio'><input type='radio' name='baselayer' id='<%= uuid %>'> <%= title %></label></li>" );
            } else {
                var html = _.template( "<li><label class='checkbox'><input type='checkbox' id='<%= uuid %>'> <%= title %></label></li>" );
            } 
            var $el = $(html(this));
            $( $el ).on("change", this, function( event ) {
                event.data.toogle();
            });
            $( "#" + this.category_slug + " ul" ).append( $el ); 
        };

        Layer.prototype.show = function() {
            if (this.category === "baselayerlist") {
                _( cedac.baselayerlist ).forEach( function( baselayer ) {
                   baselayer.hide();
                });
                this.map.addLayer( this.layer);
            } else {
                this.map.addLayer( this.layer);
                var html = _.template( "<img id='legend_<%= uuid %>' src='<%= legend %>' alt='<%= title %> - Legend'>" );
                $("#" + this.uuid).parent().after( html(this) );
            }
            this.layer.setZIndex( this.zindex );
            $("#" + this.uuid).prop("checked", true);
        }

        Layer.prototype.hide = function() {
            if ( this.map.hasLayer( this.layer ) ) this.map.removeLayer( this.layer );
            $("#" + this.uuid).prop("checked", false);
            $("#legend_" + this.uuid).remove();
        }

        Layer.prototype.toogle = function() {
            if ( $("#" + this.uuid).prop("checked") ) {
                this.show();
            } else {
                this.hide();
            }
        }

        return Layer;

    }());

})();


$( document ).ready(function() {

    var map = cedac.initMap( [42.35, -71.6], 9 );

    // add categories and overlays
    $.getJSON('/appconfig', function(data) {

        // build category menu
        // FIXME: deferred callback?
        cedac.initCategories (data.categories );

        // add map overlay layers
        cedac.initLayers( data.layers, map );
    });


    // TODO: cleanup to own or layer module
    $.getJSON('/properties', function(data) {

        var icon = new L.Icon({
            iconUrl: '/static/properties/img/home.png',
            shadowUrl: null,
            iconSize: new L.Point(32, 37),
            shadowSize: null,
            iconAnchor: new L.Point(16, 37),
            popupAnchor: new L.Point(2, -32)
        });

        var popup_html = _.template( "<b><%= name %></b><br> \
            <small><%= address %></small><br> \
            Units at risk 2015: <%= atrisk2015 %>" );

        var geoJSONLayer = L.geoJson( data, {
            pointToLayer: function( feature, latlng ) {
                return new L.Marker( latlng, {
                    icon: icon
                })
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup( popup_html( feature.properties ) );
            }
        });

        var markers = new L.MarkerClusterGroup({
            disableClusteringAtZoom: 14,
            polygonOptions: {
                color: '#008C99',
                weight: 2
            }
        }).addLayer( geoJSONLayer );

        map.addLayer(markers);

    });

});