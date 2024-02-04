$(document).ready(function () {

    // meal_recommend.js

    let map;
    let infowindow;

    async function initMap() {

        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

        // const { MarkerClusterer } = await google.maps.importLibrary("markerclusterer");

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                // 37.6267087,126.7080431
                const myLatLng = { lat: 37.60159, lng: 126.771916 };

                // 사용자의 현재 위치를 받아온다
                var currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                // 현재 위치를 기반으로 지도 그리기
                map = new google.maps.Map(document.getElementById("map"), {
                    zoom: 17,
                    center: currentLocation,
                    styles: [
                        {
                            featureType: "poi.business",
                            stylers: [{ visibility: "off" }]
                        },
                        {
                            featureType: "poi.school",
                            stylers: [{ visibility: "off" }]
                        },
                        {
                            featureType: "transit",
                            elementType: "labels.icon",
                            stylers: [{ visibility: "off" }]
                        }
                        // 여기에 더 많은 스타일 규칙을 추가할 수 있습니다.
                    ]
                });

                // new google.maps.Marker({
                //     position: myLatLng,
                //     map,
                //     title: '1231231',
                // });

                findPlace(currentLocation);

                // const service = new google.maps.places.PlacesService(map);)

                // const marker = new google.maps.Marker({
                //     title: "박천순대국",
                //     myLatLng,
                //     map,
                // });

                // const infoWindow = new google.maps.InfoWindow({
                //     content: "",
                //     disableAutoPan: true,
                // });

                // var request = {
                //     location: currentLocation,
                //     radius: '500', // 검색 반경 500미터
                //     query: 'salad',
                //     // type: ['restaurant'] // 식당만 검색
                // };

                // service.nearbySearch(request, callback); // nearbySearch를 사용하여 주변 식당 검색

                // service = new google.maps.places.PlacesService(map);
                // service.findPlaceFromQuery(request, (results, status) => {
                // if (status === google.maps.places.PlacesServiceStatus.OK && results) {
                // console.log('results : ', results)
                // for (let i = 0; i < results.length; i++) {
                //             createMarker(results[i]);
                //         }

                //         map.setCenter(results[0].geometry.location);
                //     }
                // });


            }, function () {
                handleLocationError(true, map.getCenter());
            });
        } else {
            // Browser doesn't support Geolocation
            // handleLocationError(false, map.getCenter());

        }

    }

    async function findPlace(currentLocation) {

        const request = {
            textQuery: "샐러드",
            fields: ["displayName", "location"],
            locationBias: currentLocation,
        };

        // const { places } = await google.maps.places.Place.findPlaceFromQuery(request);
        const { places } = await google.maps.places.Place.searchByText(request);

        console.log('길이가 몇인데 ? places.length :', places.length)

        if (places.length) {
            const place = places[0];
            // console.log('place 제발 나와 : ', place)
            const location = place.location;

            new google.maps.Marker({
                position: location,
                map,
                title: place.displayName,
            });

            map.setCenter(location);
        } else {
            console.log("No results");
        }
    }


    initMap();

})