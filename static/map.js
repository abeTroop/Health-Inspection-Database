let map;
let geocoder;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 34.054, lng: -118.242 },
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const fullAddress = document.querySelectorAll(".full-address");
  fullAddress.forEach((el) => {
    const address = el.textContent.trim();
    geocode(address);
  });
}

function geocode(request) {
  geocoder
    .geocode({ address: request })
    .then((result) => {
        const location = result.results[0].geometry.location;
        new google.maps.Marker({
          map: map,
          position: location,
          title: request,
        });
    })
    .catch((e) => {
      alert("Geocode was not successful for the following reason: " + e);
    });
}

window.initMap = initMap;