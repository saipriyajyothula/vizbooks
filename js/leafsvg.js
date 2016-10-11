var body = d3.select("body");
var svg = body.append("svg");
var width = window.innerWidth;
var height = window.innerHeight;
var angle = (Math.PI)/2;
var radius = 50;
var h = radius*(1-Math.cos(angle/2));
var a = 2*radius*Math.sin(angle/2);
var r = radius*Math.cos(angle/2);
var padding = {x: 2, y:2};
svg.attr("width", width)
svg.attr("height", height)
svg.style("background-color","#fff")
svg.append("path")
    .attr("d","m "+padding.x+" "+(h+padding.y)+ " a "+radius+" "+radius+", "+0+", "+0+", "+1+", "+a+" 0"+" l "+(0-a/2)+" "+r+" z")
    .attr("stroke", "#ffcdc8")
    .attr("stroke-width",2)
    .attr("fill","mistyrose")