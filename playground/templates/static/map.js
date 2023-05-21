function createMap(points, pointsrecent)
{
  var minHeat = 200; //min # of points to display heatmap of crimes instead of pin map
  var crime = new L.layerGroup();
  const map = L.map('map', {
        center: [39.299236, -76.609383],
        zoom: 11,
        scrollWheelZoom:false
        });

  // define different layers, set default to StreetView
  const basemaps = {
          StreetView: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',   {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
          Places: L.tileLayer.wms('http://ows.mundialis.de/services/service?', {layers: 'OSM-Overlay-WMS', attribution: '&copy; <a href="https://www.terrestris.de/de/openstreetmap-wms/">terrestris</a> contributors'}),
          Satellite: L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{subdomains:['mt0','mt1','mt2','mt3'], attribution: '&copy; <a href= "https://cloud.google.com/maps-platform/terms/">Google Maps</a> contributors'})
    };

  // neighborhood outlines
  var myStyle = {
      "color": '#330000',
      weight: 2,
      opacity: 0.2,
      fillOpacity: 0.2
    };
  var geojsonLayer = new L.GeoJSON.AJAX("static/neighborhood.geojson", 
  {style: myStyle,
    onEachFeature: function (feature, layer) {layer.bindPopup(feature.properties.CSA2010 + "<br>HFAI (2015): " + feature.properties.hfai15 + "<br>Median Income (2021): " + feature.properties.mhhi21);}
  });

  // reset map to default location
  L.easyButton('fa-home',function(btn, map){map.setView([39.299236, -76.609383], 11);}).addTo(map);

  // scale
  L.control.scale({position: 'bottomright'}).addTo(map);

  // crime map
  if (points.length < minHeat) // not enough data for heatmap, switch to pin map
  {
    for (let i = 0; i < points.length; ++i)
    {
      var pin = addPoint(points[i][0], points[i][1], points[i][2], points[i][3], points[i][4], 
                        points[i][5], points[i][6], points[i][7]);
      pin.addTo(crime);
    }
  }else // heatmap of crimes
  {
    var pointsTemp = [];
    for (let j = 0; j < points.length; j++)
    {
      pointsTemp.push([points[j][0], points[j][1]]);
    }
    crime = L.heatLayer(pointsTemp, {radius: 35, blur: 15});
  }
    
  // pin map of recent crimes
  var recentcrime = new L.layerGroup();
  for (let i = 0; i < pointsrecent.length; ++i)
  {
    var pin = addPoint(pointsrecent[i][0], pointsrecent[i][1], pointsrecent[i][2], pointsrecent[i][3], pointsrecent[i][4], 
                      pointsrecent[i][5], pointsrecent[i][6], pointsrecent[i][7], "red");
    pin.addTo(recentcrime);
  }
    
  // layers contol panel
  L.control.layers(basemaps, {"Neighborhoods": geojsonLayer, "Crimes": crime, "Recent Crimes": recentcrime}, {position: 'bottomleft'}).addTo(map);
  geojsonLayer.bringToBack();
  basemaps.StreetView.addTo(map); // set basemap to streetview on load
  crime.addTo(map); // show crime map on load
  return map;
}

// add pin to map
function addPoint(latitude, longitude, crimecode, description, weapon, datetime, neighborhood, location, color="blue")
{
  // message to display on popup (when marker is clicked on)
  var msg = "Crime Code: " + crimecode + "<br>Description: " + description + "<br>Weapon: " + weapon + 
            "<br>Date-time: " + datetime + "<br>Neighborhood: " + neighborhood + "<br>Location: " + location;
    
  // use red marker instead of default blue
  if (color == "red")
  {
    var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
    });     
    return L.marker([latitude, longitude], {icon: redIcon}).bindPopup(L.popup().setContent(msg));
    }
  return L.marker([latitude, longitude]).bindPopup(L.popup().setContent(msg));
}