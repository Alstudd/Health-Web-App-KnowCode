const map = L.map('map'); 
// Initializes map

map.setView([51.505, -0.09], 13); 
// Sets initial coordinates and zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map); 
// Sets map data source and associates with map

let marker, circle, zoomed;

navigator.geolocation.watchPosition(success, error);

function success(pos) {

    const lat = pos.coords.latitude;
    const lng = pos.coords.longitude;
    const accuracy = pos.coords.accuracy;

    if (marker) {
        map.removeLayer(marker);
        map.removeLayer(circle);
    }
    // Removes any existing marker and circule (new ones about to be set)

    marker = L.marker([lat, lng]).addTo(map);
    circle = L.circle([lat, lng], { radius: accuracy }).addTo(map);
    // Adds marker to the map and a circle for accuracy

    if (!zoomed) {
        zoomed = map.fitBounds(circle.getBounds()); 
    }
    // Set zoom to boundaries of accuracy circle

    map.setView([lat, lng]);
    // Set map focus to current user position

}

function error(err) {

    if (err.code === 1) {
        alert("Please allow geolocation access");
    } else {
        alert("Cannot get current location");
    }

}



// // Map initialization 
// if ('{{user.id}}' != 1) {
//     var map = L.map('map').setView([14.0860746, 100.608406], 6);

//     //osm layer
//     var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {});
//     osm.addTo(map);
        
//     if (!navigator.geolocation) {
//         console.log("Your browser doesn't support geolocation feature!")
//     } else {
//         setInterval(() => {
//             navigator.geolocation.getCurrentPosition(getPosition)
//         }, 6000);
//     }
        
//     var marker, circle;
        
//     function getPosition(position) {
//         // console.log(position)
//         var lat = position.coords.latitude
//         var long = position.coords.longitude
//         var accuracy = position.coords.accuracy
        
//         if (marker) {
//             map.removeLayer(marker)
//         }
        
//         if (circle) {
//             map.removeLayer(circle)
//         }
        
//         marker = L.marker([lat, long])
//         circle = L.circle([lat, long])
        
//         var featureGroup = L.featureGroup([marker, circle]).addTo(map)
        
//         map.fitBounds(featureGroup.getBounds())
        
//         console.log("Your coordinate is: Lat: " + lat + " Long: " + long + " Accuracy: " + accuracy)
//     }
// }