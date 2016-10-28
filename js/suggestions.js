function sim_last(similar,dummyclick){
    var simsvg = d3.select("body").append("svg")
                .attr("width", 1000)
                .attr("height", 200);

            //group
            var simgroup = simsvg.append("g")
                .attr("transform", "translate(" + margin.left + "," + -300 + ")");

            //images
            var simimages = simgroup.selectAll("image")
                .data(similar).enter();
                
            var simimgs = simimages.append("svg:image")
                .attr('class','imgs')
                .attr("xlink:href",function(d){return d.img;})
                .attr('x',function(d,i){return i%5 * 200;})
                .attr('y',300)
                .attr('width',200)
                .attr('height',200)
                .attr('opacity',0.5)
                .classed("hidden",false);


            var z = null;
            d3.selectAll(".imgs").on('click',function(d){z = d});
            //dummyclick(z);
            
}