//Margins
var margin = {top: 10, right: 50, bottom: 20, left: 50},
    width = 1500 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom;


function first_call(){
    
//Load data
d3.json("Data/img.json",function(d){
    
    i = d.value;
    d3.shuffle(i);

    var selected_imgdir = "";

    //svg

    var svg = d3.select('body').append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr('id','topsvg');
      
    
    var image_height = 115,
        image_width = 115;

    svg.append("svg:image").attr('id','home')
        .attr('xlink:href','Data/home.jpg')
        .attr('x',width - 20).attr('y',10)
        .attr('width',40).attr('height',40)
        .on("click",function(){location.reload();});


    /* Navigation
    var nav1yloc = 370,
        nav2yloc = 420;

    var tempsvg = d3.select('#topsvg').append('g')
            .attr("transform","translate(" + 60 + "," + 60 + ")")
            .style('position','fixed');

    var navi1 = tempsvg.append('circle').attr('id','navi1').attr('r',6)
                .attr('cx',1400)
                .attr('cy',nav1yloc)
                .attr('fill','white')
                .style('stroke','black');

    var navi2 = tempsvg.append('circle').attr('id','navi2').attr('r',6)
                .attr('cx',1400)
                .attr('cy',nav2yloc)
                .attr('fill','#cdd0d7')
                .style('stroke','black');

   
    d3.select('#navi2').on('click',function(){
        d3.transition()
        .delay(200)
        .duration(500)
        .tween("scroll", scrollTween(document.body.getBoundingClientRect().height - window.innerHeight));
        d3.select('#navi2').transition()
        .delay(200)
        .duration(500).attr('fill','white');
        d3.select('#navi1').transition()
        .delay(200)
        .duration(500).attr('fill','#cdd0d7')

    });

    d3.select('#navi1').on('click',function(){
        d3.transition()
        .delay(200)
        .duration(500)
        .tween("scroll", scrollTween(0));
        d3.select('#navi1').transition()
        .delay(200)
        .duration(500).attr('fill','white');
        d3.select('#navi2').transition()
        .delay(200)
        .duration(500).attr('fill','#cdd0d7')
    });

    function scrollTween(offset) {
      return function() {
        var i = d3.interpolateNumber(window.pageYOffset || document.documentElement.scrollTop, offset);
        return function(t) { scrollTo(width, i(t));
            d3.select('#navi1').attr('cy',nav1yloc + i(t));
            d3.select('#navi2').attr('cy',nav2yloc + i(t));
         };
      };
    }
    */

    //group
    var group = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    //images
    var images = group.selectAll("image")
        .data(i).enter();
    
    var imgs = images.append("svg:image")
        .attr('class','imgs')
        .attr("xlink:href",function(d){return d.img;})
        .attr('x',function(d,i){return (width - 150) - i%10 * (image_width + 15);})
        .attr('y',function(d,i){return (height - 170) - Math.floor(i/10) * (image_height + 15);})
        .attr('width',image_width)
        .attr('height',image_height)
        .attr('opacity',0.8);

    var top_label = svg.append("text")
                .attr('x',600).attr('y',30)
                .style('font-size',"30px").style('font-weight','bold')
                .attr('opacity',1);

    var label = svg.append("text")
                .attr('x',250).attr('y',50)
                .style('font-size',"20px").style('font-weight','bold')
                .attr('opacity',0);

    var auth_label = svg.append("text")
                .attr('x',650).attr('y',50)
                .style('font-size',"20px").style('font-weight','bold')
                .attr('opacity',0);

    // listener events
    var setevents = d3.selectAll('.imgs').on('mouseenter',function(d){
            d3.select(this)
            .transition()
            .attr('opacity',1)
            .attr('height',225)
            .attr('width',225);

            top_label.text(d.name).attr('opacity',1);
        })
        .on('mouseleave',function(d){
            d3.select(this)
            .transition()
            .attr('opacity',0.8)
            .attr('height',image_height)
            .attr('width',image_width);

            top_label.attr('opacity',0);
        })
        .on('click',imageclick);

        function imageclick(d){
            // hide all images except selected one (dimension change)

            top_label.remove();
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
                .on('mouseleave',null).on('click',null);

            // change svg dimensions and append text
            svg.transition().duration(800).attr("height",110);
            
            // add labels
            label.text("Book"+ "\u00A0\u00A0\u00A0\u00A0\u00A0" + d.name)
                .transition().duration(1000).attr('opacity',1);

            auth_label.text("Author"+"\u00A0\u00A0\u00A0\u00A0\u00A0"+d.author_name)
            .transition().duration(1000).attr('opacity',1);

            // get similar author books
            var similar = i.filter(function(o){
                return (o.author_name == d.author_name) && (o.name != d.name)});

            networkcall();
        }


});

}
first_call();


