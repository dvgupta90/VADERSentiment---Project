"use strict";

function displayScore(result) {
    // console.log(result);
    let score_info = result.score;
    let compound_score = score_info.compound;
    let neg_score = score_info.neg;
    let pos_score = score_info.pos;
    let neu_score = score_info.neu;
    let str = "Compound Score: "+compound_score+"; "+"Negative Score: "+neg_score+"; "+"Neutral Score: "+neu_score+"; "+"Positive Score: "+pos_score;
    $('#review-score').html(str);
    // $('#review-score').html(JSON.stringify(score_info)); 
    // we used JSON>stringify coz the analyzer returns an object and to display that on html we have to make it into a string
}

function showReview(evt) {
    evt.preventDefault();

    let url = "/process_check_your_review";
    let formData = {"review": $("#user-review").val()};
    // console.log(formData);

    $.post(url, formData, displayScore);
}

$("#senti").on('submit',showReview);

