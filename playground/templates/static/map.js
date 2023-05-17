function createMap(points, pointsrecent)
{
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
        opacity: 0.5,
        fillOpacity: 0.5
      };
    var geojsonLayer = new L.GeoJSON.AJAX("static/neighborhood.geojson", 
    {style: myStyle,
      onEachFeature: function (feature, layer) {layer.bindPopup(feature.properties.CSA2010 + "<br>HFAI (2015): " + feature.properties.hfai15 + "<br>Median Income (2021): " + feature.properties.hfai15);}
    });


    // reset map to default location
    L.easyButton('fa-home',function(btn,map){
        map.setView([39.299236, -76.609383], 11);
      }).addTo(map);

    // scale
    L.control.scale({position: 'bottomright'}).addTo(map);

    // heat map
    var heatMap = L.heatLayer(points, {radius: 50, blur: 25});
    
    // pin map of recent crimes
    var recentcrime = new L.layerGroup()
    for (let i = 0; i < pointsrecent.length; ++i)
    {
        var pin = addPoint(map, pointsrecent[i][0], pointsrecent[i][1], pointsrecent[i][2], pointsrecent[i][3], pointsrecent[i][4], 
                                pointsrecent[i][5], pointsrecent[i][6], pointsrecent[i][7]);
        pin.addTo(recentcrime);
    }
    
    // layers contol panel
    L.control.layers(basemaps, {"Neighborhoods": geojsonLayer, "Heat Map": heatMap, "Recent Crimes": recentcrime}, {position: 'bottomleft'}).addTo(map);
    basemaps.StreetView.addTo(map);
    heatMap.addTo(map);

    return map;
}


// add datapoint to map
function addPoint(map, latitude, longitude, crimecode, description, weapon, datetime, neighborhood, location)
{
    var msg = "Crime Code: " + crimecode + "<br>Description: " + description + "<br>Weapon: " + weapon + 
    "<br>Date-time: " + datetime + "<br>Neighborhood: " + neighborhood + "<br>Location: " + location;
    return L.marker([latitude, longitude]).bindPopup(L.popup().setContent(msg));
}