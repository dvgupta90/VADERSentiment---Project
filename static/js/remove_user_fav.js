"use strict";


function display_message(results){
    let showmessage = results.message;
    alert(showmessage);
    // auto refreshes page after removing fav
    window.location.reload();
// it'll take results whatever server.py file returns

}



function remove_from_fav(evt) {
  
    let payload = {
    database_rest_id:$(evt.target).data('rest-id'),
    };
  
    $.post('/remove_from_fav', payload, display_message);
   
}
// using a jquery class selector
$('.remove-fav-button').on('click', remove_from_fav);
