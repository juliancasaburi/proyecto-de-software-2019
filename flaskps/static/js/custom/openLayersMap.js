import '../../css/ol.css';
import './ol';
//import Map from 'ol/Map';
//import View from 'ol/View';
//import {easeIn, easeOut} from 'ol/easing';
//import TileLayer from 'ol/layer/Tile';
//import {fromLonLat} from 'ol/proj';
//import OSM from 'ol/source/OSM';

$(document).ready(function(){
    var lat = -34.92595;
    var lon = -57.89335;
    var zoom = 20;

    var info = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
        name: 'Escuela 25'
    });
    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon({
            crossOrigin: 'anonymous'
            //src: '{{ url_for('static', filename='img/escuela.png') }}'
        })
    });

    var vectorSource = new ol.source.Vector({
        features: [info]
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
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([lon, lat]),
            zoom: zoom
        }),
        controls: new ol.control.defaults().extend([
            new ol.control.Rotate(),
            new ol.control.MousePosition(),
            new ol.control.OverviewMap(),
            new ol.control.ZoomToExtent(),
            new ol.control.ScaleLine(),
            new ol.control.ZoomSlider()
        ])
    });
});