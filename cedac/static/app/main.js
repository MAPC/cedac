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

        var hash = new L.Hash(map);

        return map;
    }

    // initialize category menu
    function initCategories ( categories ) {
        // category menue
        // TODO: move to html template
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

    // initialize layers
    function initLayers( layers, map) {
        _( layers ).forEach( function( layer ) {

            // Leaflet Layer Object or new WMS layer
            if ( _.has(layer, 'layer') ) {
                var llLayer = layer.layer;
            } else if ( _.has(layer, 'wms') ) {
                var llLayer = L.tileLayer.wms( layer.wms.url , {
                    layers: layer.wms.layers,
                    styles: layer.wms.styles,
                    format: layer.wms.format,
                    transparent: layer.wms.transparent,
                    attribution: layer.wms.attribution
                });
                llLayer.setOpacity(0.4);

                // strip out GWC caching service from WMS url 
                // GWC service doesn't provide legend image
                var legendUrl = layer.wms.url;
                var regex = /\/gwc\/service/;
                if (legendUrl.match(regex)) {
                    legendUrl = legendUrl.replace(regex, "");
                }
                var legend = legendUrl + "?VERSION=1.1.0&REQUEST=GetLegendGraphic&FORMAT=image/png&legend_options=fontAntiAliasing&LAYER=" + layer.wms.layers;
            }
            var legend = legend || "";

            // instantiate new Layer
            var options = _.assign( layer , { 'layer': llLayer, 'legend': legend, 'map': map });
            var maplayer = new cedac.Layer( options );

            // keep track of baselayers
            if ( layer.category === "baselayerlist" ) {
                cedac.baselayerlist.push( maplayer );
            }  
            if (layer.visible) maplayer.show();
        });
    }

    // resize map (and sidebar accordingly) between 8 and 12 columns
    var mapwidths = [ 'span8', 'span12' ];
    function resize( map, mapcontainer, sidebar, oldheight ) {
        $( mapcontainer ).removeClass( mapwidths[0] ); // oldwith
        $( mapcontainer ).addClass( mapwidths[1] ); // newwidth

        if ( mapwidths[1] === 'span12' ) { // larger map
            var mapheight = $(window).height() - 250,
                btn = {
                    btntext : 'Smaller Map',
                    btnicon : 'icon-resize-small'
                };
                mapheight = mapheight < 500 ? '500px' : mapheight + 'px';
                $( sidebar ).addClass('hide-sidebar');
            // TODO: redraw basemap
        } else {
            var mapheight = '500px',
                btn = {
                    btntext : 'Larger Map',
                    btnicon : 'icon-resize-full'
                };
            $( sidebar ).removeClass('hide-sidebar');
        }

        mapwidths.reverse();

        var btn_html = _.template( '<i class="<%= btnicon %>"></i> <%= btntext %>' );
        $("#resize-btn").html( btn_html( btn ) )
        // FIXME: map shouldn't be hardcoded
        $( "#map" ).css( 'height', mapheight );

        map.invalidateSize( true );
    }


    // expose functions
    cedac.initMap = initMap;
    cedac.initLayers = initLayers;
    cedac.initCategories = initCategories;
    cedac.resize = resize;

    // baselayers are radios, only one visible at a time
    cedac.baselayerlist = [];

    // Layer module
    // TODO: maybe extend L.Class (http://leafletjs.com/reference.html#ilayer) instead?
    cedac.Layer = (function() {

        // initial
        var Layer = function( options ) {
            this.layer = options.layer;
            this.title = options.title;
            this.category = options.category;
            this.category_slug = options.category.toLowerCase().replace(" ", "_");
            this.map = options.map;
            this.uuid = _.uniqueId( this.category_slug + "_" );
            this.legend = options.legend;
            this.zindex = options.zindex

            // add layer to appropriate category
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
                this.map.addLayer( this.layer );
            } else {
                // add layer legend image in sidebar
                this.map.addLayer( this.layer);
                var html = _.template( "<img class='legend <%= uuid %>' src='<%= legend %>' alt='<%= title %> - Legend'>" );
                $( "#" + this.uuid ).parent().after( html( this ) );
                // and to print legend
                var print_html = _.template( "<li><%= title %></br><img class='<%= uuid %>' src='<%= legend %>' alt='<%= title %> - Legend'></li>" );
                $( ".print-legend ul" ).append( print_html( this ) );
            }
            this.layer.setZIndex( this.zindex );
            $( "#" + this.uuid ).prop( "checked", true );
        }

        Layer.prototype.hide = function() {
            if ( this.map.hasLayer( this.layer ) ) this.map.removeLayer( this.layer );
            $( "#" + this.uuid ).prop( "checked", false );
            $( ".sidebar .legend." + this.uuid ).remove();
            $( ".print-legend ." + this.uuid ).parent().remove();
        }

        Layer.prototype.toogle = function() {
            if ( $("#" + this.uuid).prop( "checked" ) ) {
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

    // map tools
    $( '#resize-btn' ).on( 'click', function() {
        var oldheight = $( '#map' ).height();
        cedac.resize( map, '.mapcontainer', '.sidebar', oldheight );
    });
    $( '#email-btn' ).on( 'click', function() {
        $( this ).attr( 'href', 'mailto:?subject=CEDAC Expiring Use Properties&body=' + document.URL );
    });
    $( '#print-btn' ).on( 'click', function() {
        $( '.print-legend p:first-child' ).text( document.URL );
        window.print();
    });

    // add categories and overlays
    $.getJSON('/appconfig', function( data ) {

        // build category menu
        // FIXME: deferred callback for layers when categories are rendered?
        cedac.initCategories( data.categories );

        // add map overlay layers
        cedac.initLayers( data.layers, map );
    });


    // load CEDAC properties into property layer
    // TODO: cleanup to own or layer module
    $.getJSON('/properties', function( data ) {

        var icon = new L.Icon({
            iconUrl: '/static/properties/img/home.png',
            shadowUrl: null,
            iconSize: new L.Point(32, 37),
            shadowSize: null,
            iconAnchor: new L.Point(16, 37),
            popupAnchor: new L.Point(2, -32)
        });

        var popup_html = _.template(
            $( 'script.map-popup' ).html()
        );

        
        
        var onClick = function (e) {
            var target = e.target;
            // var coords = new L.LatLng(target._latlng.lat, target._latlng.lng)
            var data = $( '#data' );
            var datalist = $( 'a#dataarea.accordion-toggle.collapsed' );
            // var marker = L.marker(coords).addTo(map);
            data.html( popup_html( target.feature.properties ) );
            datalist.removeClass('green');
            datalist.trigger('click');
            // map.panTo(coords);
        }

        var onEachFeature = function (feature, layer){
            // layer.bindPopup( popup_html( feature.properties ) );
            layer.on({
                click: onClick
            });
        };

        var geoJSONLayer = L.geoJson( data, {
            pointToLayer: function( feature, latlng ) {
                return new L.Marker( latlng, {
                    icon: icon
                })
            },
            onEachFeature: onEachFeature
        });

        var markers = new L.MarkerClusterGroup({
            disableClusteringAtZoom: 12,
            iconCreateFunction: function ( cluster ) {
                return new L.DivIcon({ html: '<div>' + cluster.getChildCount() + '</div>', className: 'cedac-cluster', iconSize: new L.Point(40, 40) });
            },
            showCoverageOnHover: false,
            polygonOptions: {
                color: '#008C99',
                weight: 2
            },
            maxClusterRadius: 100
        }).addLayer( geoJSONLayer );

        map.addLayer( markers );

    });

});