
async function weatherMap(){
    let weatherId = document.getElementById('weather-data')
    let weatherData = JSON.parse(weatherId.textContent);

    if(weatherData){
        console.log("starting");
        const lat = weatherData.coord.lat;
        const lon = weatherData.coord.lon;

        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
        
        const map = new Map(document.getElementById("location-map"), {
            center: { lat: lat, lng: lon },
            zoom: 8,
            mapId: "4504f8b37365c3d0",
            mapTypeId: 'terrain',
            disableDefaultUI: true,
            zoomControl: true,
        });

        new AdvancedMarkerElement({
            position: { lat: lat, lng: lon },
            map: map,
            title: weatherData.name,
        });

        const overlay = new google.maps.ImageMapType({
            getTileUrl: function(coord, zoom) {
                return `https://tile.openweathermap.org/map/precipitation_new/${zoom}/${coord.x}/${coord.y}.png?appid={WEATHER_API_KEY}`;
            },

            tileSize: new google.maps.Size(256, 256),
            opacity: 0.4
        });

        map.overlayMapTypes.insertAt(0, overlay);

        console.log("map somehow");
    }

    console.log("mapped it");  
}



window.addEventListener('load', weatherMap);
console.log("mapped out");
