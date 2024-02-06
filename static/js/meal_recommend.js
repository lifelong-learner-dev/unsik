$(document).ready(function () {

    let map;
    let isinitMap = true;
    let latitude = 0.0
    let longitude = 0.0


    async function initMap(menuItemText) {

        // 호출
        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

        // const { MarkerClusterer } = await google.maps.importLibrary("markerclusterer");

        if (navigator.geolocation) {

            navigator.geolocation.getCurrentPosition(function (position) {
                // console.log('여기 못오는거지 ?')
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
                    zoom: 15,
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
                // console.log('views.py에서  잘 오니 ?  : ')
                findPlace(currentLocation, menuItemText);



            }, function (err) {
                // handleLocationError(true, map.getCenter());
                fetchUserLocationFallback();
                console.log('err :', err)
            });
        } else {
            // Browser doesn't support Geolocation
            // console.log('여기 오면 안되는데...')
            // handleLocationError(false, map.getCenter());

        }
    }

    async function initMap2(loc1, loc2, menuItemText) {
        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

        // console.log('여기 들어오니 이제  ?');

        // 사용자의 현재 위치를 받아온다
        var currentLocation = {
            lat: loc1,
            lng: loc2
        };

        // 현재 위치를 기반으로 지도 그리기
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 15,
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
        // console.log('views.py에서  잘 오니 ?  : ')
        findPlace(currentLocation, menuItemText);




    }

    async function findPlace(currentLocation, seachText) {

        // console.log('seachText :', seachText)

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

            // console.log('ㅎㅇ ?  : ', isinitMap);

            if (isinitMap) {

                initMap(menuItemText);
            } else {
                initMap2(latitude, longitude, menuItemText)
            }
        });
    });

    function fetchUserLocationFallback() {
        fetch("https://ipinfo.io/json")
            //     console.log('response.json()' , response.json());
            // })
            // .catch(error => console.log('error', error));

            // fetch('https://ipinfo.io/json?token=YOUR_TOKEN_HERE')
            .then(response => response.json())
            .then(data => {
                // loc 속성에서 위도와 경도 추출
                isinitMap = false;
                const loc = data.loc.split(','); // loc 문자열을 쉼표로 분리하여 배열로 변환
                latitude = parseFloat(loc[0]); // 배열의 첫 번째 요소(위도)를 실수로 변환
                longitude = parseFloat(loc[1]); // 배열의 두 번째 요소(경도)를 실수로 변환

                // console.log(`위도: ${latitude}, 경도: ${longitude}`);

                initMap2(latitude, longitude, ' ')

                // 여기에서 latitude와 longitude를 사용하여 필요한 작업을 수행하세요.
                // 예를 들어, Google Maps API를 사용하여 지도에 마커를 추가하거나, 지도 중심을 이동시킬 수 있습니다.
            });
    }


    initMap(' ');

});
