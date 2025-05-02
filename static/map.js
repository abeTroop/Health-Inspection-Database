let map;
let geocoder;
let infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 34.054, lng: -118.242 },
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const facilityID = document.querySelectorAll(".facility-id");
  const facilityName = document.querySelectorAll(".facility-name");
  const fullAddress = document.querySelectorAll(".full-address");

  for (let i = 0; i < fullAddress.length; i++) {
    const address = fullAddress[i].textContent.trim();
    const name = facilityName[i].textContent.trim();
    const id = facilityID[i].textContent.trim();
    geocode(address, name, id);
  }

  infoWindow = new google.maps.InfoWindow();
}

function geocode(request, name, id) {
  geocoder
    .geocode({ address: request })
    .then((result) => {
        const location = result.results[0].geometry.location;
        const newMarker = new google.maps.Marker({
          map: map,
          position: location,
          title: request,
        });

        newMarker.addListener("click", () => {
            infoWindow.setContent(`
                <div class="restaurant-info">
                    <div>
                        <strong>${name}</strong>
                    </div>
                    <div>
                        ${request}
                    </div>
                    <a href="/facility/${id}">
                        <p>View Inspections</p>
                    </a>
                </div>
            `);
            infoWindow.open(map, newMarker);
        });
    })
    .catch((e) => {
      alert("Geocode was not successful for the following reason: " + e);
    });
}

window.initMap = initMap;