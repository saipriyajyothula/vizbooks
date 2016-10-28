//Margins
var margin = {top: 10, right: 50, bottom: 20, left: 50},
    width = 1200 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;

// var glob_tog = false;

function first_call(){
    
    //Load data
d3.json("Data/img.json",function(d){
    
    i = d.value;
    d3.shuffle(i);

    var selected_img = "";

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
        .attr('class','imgs')
        .attr("xlink:href",function(d){return d.img;})
        .attr('x',function(d,i){return (width - 300) - i%5 * 200;})
        .attr('y',function(d,i){return (height - 700) - Math.floor(i/5) * 200;})
        .attr('width',200)
        .attr('height',200)
        .attr('opacity',0.5);

    /*
    var labels = images.append('Text').text(function(d){return d.img;})
                .attr('dx',".5em").attr('dy',".5em")
                .style("font-size","11px");
    */
    var label = svg.append("text")
                .attr('x',300).attr('y',50)
                .style('font-size',"20px").style('font-weight','bold')
                .attr('opacity',0);

    var auth_label = svg.append("text")
                .attr('x',600).attr('y',50)
                .style('font-size',"20px").style('font-weight','bold')
                .attr('opacity',0);


    // listener events
    var setevents = d3.selectAll('.imgs').on('mouseenter',function(){
            d3.select(this)
            .transition()
            .attr('opacity',1)
            .attr('height',300)
            .attr('width',300);
        })
        .on('mouseleave',function(){
            d3.select(this)
            .transition()
            .attr('opacity',0.5)
            .attr('height',200)
            .attr('width',200);
        })
        .on('click',imageclick);

        /*
        function dummyclick(d){
            // hide all images except selected one (dimension change)
            imgs.classed('hidden',true);

            d3.select(this)
                .classed("hidden",false)
                .transition()
                .duration(600)
                .attr('width',100)
                .attr('height',100)
                .delay(100)
                .attr('x',0)
                .attr('y',0);
            
            // remove listeners
            d3.selectAll(".imgs").on('mouseenter',null)
            .on('mouseleave',null);

            // change svg dimensions and append text
            svg.transition().duration(800).attr("height",150);
            
            // add labels
            label.text(d.name)
            .transition().duration(1000).attr('opacity',1);

            auth_label.text(d.author_name)
            .transition().duration(1000).attr('opacity',1);


            // get similar author books
            var similar = i.filter(function(o){
                return (o.author_name == d.author_name) && (o.name != d.name)});

            networkcall(similar,dummyclick);
        }
        */

        function imageclick(d){
            // hide all images except selected one (dimension change)
            imgs.classed('hidden',true);

            d3.select(this)
                .classed("hidden",false)
                .transition()
                .duration(600)
                .attr('width',100)
                .attr('height',100)
                .delay(100)
                .attr('x',0)
                .attr('y',0);
            
            // remove listeners
            d3.selectAll(".imgs").on('mouseenter',null)
                .on('mouseleave',null);

            // change svg dimensions and append text
            svg.transition().duration(800).attr("height",150);
            
            // add labels
            label.text(d.name)
                .transition().duration(1000).attr('opacity',1);

            auth_label.text(d.author_name)
            .transition().duration(1000).attr('opacity',1);


            // get similar author books
            var similar = i.filter(function(o){
                return (o.author_name == d.author_name) && (o.name != d.name)});

            networkcall();
        }

        /*
        if(glob_tog == true){
            dummyclick(d);
        }
        */

});

}
first_call();


