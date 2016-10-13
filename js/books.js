// set the dimensions and margins of the graph
var margin = {top: 20, right: 20, bottom: 20, left: 20};
var width = 960 - margin.left - margin.right;
var height = 960 - margin.top - margin.bottom; 


// set the width and height to window dimensions and position the group element
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("background-color","#fff")

var g = svg.append("g")
    .attr("transform", "translate(" + (width/2 + margin.left) + "," + (height/2 + margin.top)+ ")");
