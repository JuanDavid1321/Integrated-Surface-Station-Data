import coordenadas from './coords.js'

let paisReferencia = 'US';

// Define una función que reciba el nombre del país y devuelva las coordenadas geográficas correspondientes
const obtenerCoordenadas = pais => coordenadas[pais];

// Crear un nuevo mapa con OpenLayers
let map = new ol.Map({
  target: 'map', // Selección por ID
  layers: [
    new ol.layer.Tile({source: new ol.source.OSM()})
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat(obtenerCoordenadas(paisReferencia)),
    zoom: 5
  })
});

// Función para agregar puntos en coordenadas específicas del mapa, con ayuda de OpenLayers
function agregarEstacion(longitude, latitude) {
  // Crea una característica de punto con la geometría especificada
  var pointFeature = new ol.Feature({
      geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
  });

  // Crea una capa de vector con la característica y el estilo personalizado
  var vectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
    features: [pointFeature],
    }),
    style: () => new ol.style.Style({
      // Forma de círculo
      image: new ol.style.Circle({
        radius: 4,
        // Color relleno
        fill: new ol.style.Fill({
          color: 'red',
        }),
        // Color de borde
        stroke: new ol.style.Stroke({
          color: 'black',
          width: 2,
        }),
      }),
    }),
  });

  // Agrega la capa al mapa
  map.addLayer(vectorLayer);
}


// Recorrer json con JS
fetch('/result.json')
  .then(response => response.json())
  .then(data => {
    paisReferencia = data[0].country;

    // Actualiza la vista del mapa con el nuevo centro
    map.getView().setCenter(ol.proj.fromLonLat(obtenerCoordenadas(paisReferencia)));

    // Recorre el array y crea los puntos
    data.forEach(point => {
      agregarEstacion(point.longitud, point.latitude);
    });
  });
