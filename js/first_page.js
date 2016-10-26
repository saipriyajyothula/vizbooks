//Margins
var margin = {top: 10, right: 50, bottom: 20, left: 50},
    width = 1000 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;

//Load data
d3.json("img.json",function(d){
	
    i = d.value;

	//svg
	var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)

  	//group
    var group = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //images
	var images = group.selectAll("image")
    	.data(i).enter();
		
	var imgs = images.append("svg:image")
        .attr("xlink:href",function(d){return d.img;})
        .attr('x',function(d,i){return (width - 400) - i * 200;})
        .attr('y',0)
        .attr('width',200)
        .attr('height',200)
        .attr('opacity',0.5);

    var setevents = imgs.on('mouseenter',function(){
            d3.select(this)
            .transition()
            .attr('opacity',1)
            .attr('height',300)
            .attr('width',300);
        })
        .on('mouseleave',function(){
            d3.select(this)
            .transition()
            .attr('opacity',0.3)
            .attr('height',200)
            .attr('width',200);
        })
        .on('click',function(){
            svg.attr('x',50)
            .attr('height',20)
            .attr('width',20);

        group
            .attr("transform", "translate(" + 50 + "," + 0 + ")");
        });
        

});
