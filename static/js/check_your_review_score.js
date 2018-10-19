"use strict";

function displayScore(result) {
    console.log(result);
    let score_info = result.score;
    $('#review-score').html(JSON.stringify(score_info)); 
    // we used JSON>stringify coz the analyzer returns an object and to display that on html we have to make it into a string
}

function showReview(evt) {
    evt.preventDefault();

    let url = "/process_check_your_review";
    let formData = {"review": $("#user-review").val()};
    console.log(formData);

    $.get(url, formData, displayScore);
}

$("#senti").on('submit',showReview);

