$(document).ready(function () {

    let map;

    async function initMap(menuItemText) {

        // 호출
        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

        // const { MarkerClusterer } = await google.maps.importLibrary("markerclusterer");

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                // 37.6267087,126.7080431
                // 테스트용
                // const myLatLng = { lat: 37.60159, lng: 126.771916 };

                // 사용자의 현재 위치를 받아온다
                var currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                // 현재 위치를 기반으로 지도 그리기
                map = new google.maps.Map(document.getElementById("map"), {
                    zoom: 14,
                    center: currentLocation,
                    styles: [
                        // 쓸데없는 마커들 지우기
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
                // console.log('views.py에서  잘 오니 ?  : ', searchText)
                findPlace(currentLocation, menuItemText);



            }, function () {
                handleLocationError(true, map.getCenter());
            });
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, map.getCenter());

        }

    }

    async function findPlace(currentLocation, seachText) {

        const request = {
            textQuery: seachText,
            // textQuery: '치킨',
            fields: ["displayName", "location", "businessStatus", "photos", "plusCode"],
            includedType: "restaurant",
            // maxResultCount: 5,
            locationBias: currentLocation,
        };

        // service = new google.maps.places.PlacesService(map);
        // service.nearbySearch(request, callback);

        // const { places } = await google.maps.places.Place.findPlaceFromQuery(request);
        const { places } = await google.maps.places.Place.searchByText(request);
        // const { places } = await google.maps.places.Place.textSearch(request);

        // console.log('길이가 몇인데 ? places :', places)

        if (places.length) {
            for (var i = 0; i < places.length; i++) {
                const place = places[i];
                // console.log('place info : ', place)
                const location = place.location;

                new google.maps.Marker({
                    position: location,
                    map,
                    title: place.displayName,
                });

                // map.setCenter(location);

                // 4개정도만 그리자
                if (i === 3)
                    break;
            }
        } else {
            // console.log("No results");
            if (seachText != ' ')
                alert('검색 결과가 없습니다.')
        }

        // 이건 하나만 그릴때
        // if (places.length) {
        //     const place = places[0];
        //     const location = place.location;

        //     new google.maps.Marker({
        //         position: location,
        //         map,
        //         title: place.displayName,
        //     });

        //     map.setCenter(location);
        // } else {
        //     console.log("No results");
        // }
    }

    // item을 클릭했을때 표시 
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function () {

            document.querySelectorAll('.menu-item').forEach(i => {
                i.classList.remove('clicked-item');
            });
            this.classList.add('clicked-item');
            var menuItemText = this.textContent;

            initMap(menuItemText);
        });
    });


    initMap(' ');

});

// 일단 안씀
// function callback(results, status) {
//     if (status == google.maps.places.PlacesServiceStatus.OK) {
//         for (var i = 0; i < results.length; i++) {
//             createMarker(results[i]);
//         }
//     }
// }
