function createMap()
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
    L.control.layers(basemaps, null, {position: 'bottomleft'}).addTo(map);
    basemaps.StreetView.addTo(map)

    // reset map to default location
    L.easyButton('fa-home',function(btn,map){
        map.setView([39.299236, -76.609383], 11);
      }).addTo(map);

    // scale
    L.control.scale({position: 'bottomright'}).addTo(map);

    return map;
}

// add datapoint to map
// to do: change marker icon, import info from db
function addPoint(map, latitude, longitude, crimecode, description, weapon, datetime, neighborhood)
{
    var msg = "Crime Code: " + crimecode + "<br>Description: " + description + "<br>Weapon: " + weapon + 
    "<br>Date-time: " + datetime + "<br>Neighborhood: " + neighborhood;
    L.marker([latitude, longitude]).bindPopup(L.popup().setContent(msg)).addTo(map);
}