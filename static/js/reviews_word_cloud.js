var review_words_scale = d3.scale.linear().range([10,60]);

var width = 750;
var height = 750;

var color = d3.scale.linear().interpolate(d3.interpolate)
      .range([d3.rgb("#ff0000"), d3.rgb('#00ff00')]);
var review_data = "global";

d3.csv("/static/js/dict_trial.csv", function(data){
  // review_data = data
  console.log(data)
  var review_words = data
  .map(function(d){ return {text: d.word, size: +d.score}; })
  // console.log(review_words["word"])
  review_words_scale.domain([
    d3.min(review_words, function(d){return d.size}),
    d3.max(review_words, function(d){return d.size})
  ]);
  d3.layout.cloud()
    .size([500, 500])
    // .words(data.word.map(function (d){
    //   return {text: d, size: 10 + Math.random() * 90, test: "haha"};
    // }))
    .words(review_words)
    .padding(0)
    // .rotate(function() { return ~~(Math.random() * 2) * 90; })
    .font("Impact")
    .fontSize(function(d) { return review_words_scale(d.size); })
    .on("end", draw).start();

});



function draw(words) {
  d3.select("#word_cloud").append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("font-family", "Impact")
      .style("fill", function(d, i) { return color(i); })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; });
}