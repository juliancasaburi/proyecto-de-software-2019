$(document).ready(function(){
    // get nucleos activos
    var nucleos;
    $.ajax({
        type: "GET",
        url: document.getElementById("scriptMapa").getAttribute("data-ajaxURL"),
        success: function (response) {
            nucleos = response;
            nucleos_markers = [];
            for (var i=0; i<nucleos.length; i++) {
                $('#map-select').append("<option value='"+ i + "'>" + nucleos[i]['nombre'] + "</option>");
                // markers
                nucleos_markers[i] = new ol.Feature({
                    geometry: new ol.geom.Point(
                        ol.proj.fromLonLat([nucleos[i]['lng'],nucleos[i]['lat']])
                    ),
                    nucleo_pos: i
                });
                // add marker
                nucleos_markers[i].setStyle(
                    new ol.style.Style({
                        image: new ol.style.Icon({
                            anchor: [0.5, 0.0],
                            color: 'red',
                            crossOrigin: 'anonymous',
                            anchorOrigin: 'bottom-left',
                            scale: 0.4,
                            src: document.getElementById("scriptMapa").getAttribute("data-locationImg"),
                        }),
                    })
                );
            }

            $('#map-select').val("");
            $('#map-select').formSelect();

            var zoom = 15;

            var escuela_25 = [-57.89335, -34.92595];

            var info = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat(escuela_25)),
                name: 'Escuela 25'
            });
            var iconStyle = new ol.style.Style({
                image: new ol.style.Icon({
                    crossOrigin: 'anonymous',
                    src: document.getElementById("scriptMapa").getAttribute("data-flagImg"),
                })
            });

            var vectorSource = new ol.source.Vector({
                features: [info]
            });

            var vectorSourceMarkers = new ol.source.Vector({
                features: nucleos_markers
            });

            var map = new ol.Map({
                target: 'map',
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM()
                    }),
                    new ol.layer.Vector({
                        source: vectorSource,
                        updateWhileAnimating: true,
                        updateWhileInteracting: true,
                        style: function(feature, resolution) {
                            iconStyle.getImage().setScale(1/Math.pow(resolution, 1/6));
                            return iconStyle;
                        }
                    }),
                    // layer para markers
                    new ol.layer.Vector({
                        source: vectorSourceMarkers
                    })
                ],
                view: new ol.View({
                    center: ol.proj.fromLonLat(escuela_25),
                    zoom: zoom
                }),
                controls: new ol.control.defaults().extend([
                    new ol.control.Rotate(),
                    new ol.control.OverviewMap(),
                    new ol.control.ZoomToExtent(),
                    new ol.control.ScaleLine(),
                    new ol.control.ZoomSlider()
                ])
            });

            // marker onhover
            var feature_onPointerMove;
            var feature_info = document.getElementById('feature-info');
            var feature_info_jquery = $('#feature-info');
            var overlay = new ol.Overlay({
                element: feature_info,
                offset: [0, 0]
            });
            map.addOverlay(overlay);

            map.on('pointermove', function(evt) {
                feature_onPointerMove = map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
                    if (feature != info) return feature;
                });

                if (feature_onPointerMove) {
                    overlay.setPosition(evt.coordinate);

                    // texto dentro del feature
                    feature_info_jquery.show();
                    var nucleo = nucleos[feature_onPointerMove.getProperties()['nucleo_pos']];
                    var tel = nucleo['telefono'];
                    if (nucleo['telefono'] == '') tel = 'no registrado';
                    feature_info.innerHTML =
                        '<div style="margin-bottom: auto" class="row">' +
                        '<div class="col s12 center-align">' +
                        '<span><b>' + nucleo['nombre'] + '</b></span>' +
                        '</div>' +
                        '<div class="divider-feature-info div-transparent col s12"></div>' +
                        '</div class="col s12 center-align">' +
                        '<span><i style="font-size: small" class="material-icons">label</i> Teléfono: ' + tel + '</span>' +
                        '</div>' +
                        '</div>';

                    // ajustar posición del feature-info
                    var coords = feature_onPointerMove.getGeometry().getCoordinates();
                    var pixel = map.getPixelFromCoordinate(coords);
                    var map_size = map.getSize();
                    if ((pixel[0] < map_size[0]/2) && (pixel[1] < map_size[1]/2)) {
                        overlay.setOffset([0, 0]);
                        overlay.setPositioning('top-left');
                    }
                    else if ((pixel[0] < map_size[0]/2) && (pixel[1] > map_size[1]/2)) {
                        overlay.setOffset([0, 0]);
                        overlay.setPositioning('bottom-left');
                    }
                    else if ((pixel[0] > map_size[0]/2) && (pixel[1] < map_size[1]/2)) {
                        overlay.setOffset([feature_info.offsetWidth/2, 0]);
                        overlay.setPositioning('top-right');
                    }
                    else if ((pixel[0] > map_size[0]/2) && (pixel[1] > map_size[1]/2)) {
                        overlay.setOffset([feature_info.offsetWidth/2, 0]);
                        overlay.setPositioning('bottom-right');
                    }
                }
                else feature_info_jquery.hide();
            });

            // mover posición al núcleo seleccinado en el select
            $('#map-select').on('change', function() {
                var coords = [nucleos[parseInt($(this).val())]['lng'], nucleos[parseInt($(this).val())]['lat']];
                map.getView().animate({
                    center: ol.proj.fromLonLat(coords),
                    duration: 2000,
                    zoom: zoom
                })
            });

        },
        error: function (jqXhr, textStatus, errorMessage) {
            console.log("Error: ", errorMessage);
        }
    });


});