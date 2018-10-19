"use strict";


function initMap() {

    let myImageURL = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    let restaurant = {lat: $('#map').data('lat'), 
        lng: $('#map').data('lng')};
    let map = new google.maps.Map(document.querySelector('#map'), {
        center: restaurant,
        zoom: 8,
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


}

let marker = new google.maps.Marker({
  position: restaurant,
  map: map,
  icon: myImageURL

    