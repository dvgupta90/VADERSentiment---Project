var review_words_scale = d3.scaleLinear().range([20,60]);
var review_color_scale = d3.scaleLinear().range([0,1]);

var width = window.innerWidth * 0.75;
var height = 600;


var review_data = "global";

// d3.csv("/static/js/dict_trial.csv", function(data){

let foo = d3.csv("/static/js/dict_trial.csv", function(d) {
  // Map csv data onto a data object
  return { 
    text: d.word, 
    size: +d.score, 
    color: null 
  }; 
}).then(function(review_words) {

  // Create domain for data size (largest and smallest values in data set)
  review_words_scale.domain([
    d3.min(review_words, function(d){return Math.abs(d.size); }),
    d3.max(review_words, function(d){return Math.abs(d.size); })
  ]);

  // Create domain for data color
  review_color_scale.domain([
    d3.min(review_words, function(d){return d.size; }),
    d3.max(review_words, function(d){return d.size; })
  ]);

  console.log(review_color_scale.domain());
  console.log(review_color_scale.range());
  // Set color property for each data object
  
  review_words.map(function(d) {
      let t = review_color_scale(d.size);
      d.color = d3.interpolateRdYlGn(t);
      return d;
  });
  
  console.log(review_words);

  d3.layout.cloud()
    .size([1100, 600])
    // .words(data.word.map(function (d){
    //   return {text: d, size: 10 + Math.random() * 90, test: "haha"};
    // }))
    .words(review_words)
    .padding(10)
    .rotate(function() { return ~~(Math.random() * 2) * 90; })
    .text(function(d) { return d.text; })
    .fontSize(function(d) { return review_words_scale(Math.abs(d.size)); })
    .on("end", draw).start();

});

  



function draw(words) {
  d3.select("#word_cloud").append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + (width * 0.50 )+ "," + (height * 0.50) + ")")
    .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return Math.abs(d.size) + "px"; })
      .style("font-family", "Impact")
      // .style("fill", function(d, i) { return color(i); }) // FIX
      .style("fill", function(d) { return d.color; })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; });
}