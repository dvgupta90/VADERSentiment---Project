"use strict";


function display_message(results){
    let message = results;
    alert(message);

// it'll take results whatever server.py file returns

}


function add_to_fav() {
    let payload = {
    yelp_biz_id = $('#add-to-fav-button').data('id');
    yelp_rest_name = $('#add-to-fav-button').data('name');
    yelp_category = $('#add-to-fav-button').data('category');
    yelp_price = $('#add-to-fav-button').data('price');
    yelp_image_url = $('#add-to-fav-button').data('image');
    }
    $.post('/add_to_fav', payload, display_message);
}

$('#add-to-fav-button').on('click', add_to_fav);