"use strict";


function display_message(results){
    let showmessage = results.message;
    alert(showmessage);
// it'll take results whatever server.py file returns

}


// function disable(evt) {
//     $(evt.target).removeClass("waves-effect waves-light").addClass('disabled');
// }

function add_to_fav(evt) {
    let payload = {
    yelp_biz_id:$(evt.target).data('id'),
    yelp_rest_name:$(evt.target).data('name'),
    yelp_rating:$(evt.target).data('rating'),
    yelp_category:$(evt.target).data('category'),
    yelp_price:$(evt.target).data('price'),
    yelp_image_url:$(evt.target).data('image'),
    };

    $.post('/add_to_fav', payload, display_message);
    // disable(evt)
}
// using a jquery class selector
$('.add-to-fav-button').on('click', add_to_fav);





