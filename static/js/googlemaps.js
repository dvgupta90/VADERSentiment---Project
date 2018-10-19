"use strict";


function initMap() {

    
    let restaurant = {lat: $('#map').data('lat'), 
        lng: $('#map').data('lng')};
    let map = new google.maps.Map(document.querySelector('#map'), {
        center: restaurant,
        zoom: 10,
        
    // Note: the following are marked the opposite of the default setting
    // (that is, they're marked "false" if they're true by
    // default, and "true" if they're false by default) so that
    // uncommenting the following lines will actually change the map

    mapTypeControl: true,
    zoomControl: true,
    scaleControl: true,
    streetViewControl: false,
    rotateControl: true, // only available for locations with 45° imagery
    fullscreenControl: true

    });


    let marker = new google.maps.Marker({
      position: restaurant,
      map: map,
      animation:google.maps.Animation.DROP,

    });  

    let trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);

    let styles = [
  {
      "featureType": "water",
      "stylers": [
        { "color": "#2529da" }
      ]
    }

  ];

  let styledMapOptions = {
      name: 'Custom Style'
  };

  let customMapType = new google.maps.StyledMapType(
          styles,
          styledMapOptions);

  map.mapTypes.set('map_style', customMapType);
  map.setMapTypeId('map_style');

}


    