function createMap()
{
    const map = L.map('map', {
        center: [39.299236, -76.609383],
        zoom: 12,
        scrollWheelZoom:false
        });

    // define different layers, set default to StreetView
    // Todo: different/better layers?
    const basemaps = {
            StreetView: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',   {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
            //Topography: L.tileLayer.wms('http://ows.mundialis.de/services/service?',   {layers: 'TOPO-WMS'}),
            Places: L.tileLayer.wms('http://ows.mundialis.de/services/service?', {layers: 'OSM-Overlay-WMS', attribution: '&copy; <a href="https://www.terrestris.de/de/openstreetmap-wms/">terrestris</a> contributors'}),
            Satellite: L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{subdomains:['mt0','mt1','mt2','mt3'], attribution: '&copy; <a href= "https://cloud.google.com/maps-platform/terms/">Google Maps</a> contributors'})
            //Terrain: L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{subdomains:['mt0','mt1','mt2','mt3']}),
            //Hybrid: L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}),
            //Streets: L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']})
    };
    L.control.layers(basemaps, null, {position: 'bottomleft'}).addTo(map);
    basemaps.StreetView.addTo(map)

    // reset map to default location
    L.easyButton('fa-home',function(btn,map){
        map.setView([39.299236, -76.609383], 12);
      }).addTo(map);

    // scale
    L.control.scale({position: 'bottomright'}).addTo(map);

    return map;
}

// add datapoint to map
// to do: change marker icon, import info from db
function addPoint(map)
{
    const marker1 = L.marker([39.3, -76.6]).bindPopup('Crime Bad').addTo(map);
}
