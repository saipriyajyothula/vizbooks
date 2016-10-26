function force(graph){
  var width = 750,
      height = 650,
      radius = 6;

  var svg = d3.select("body").append("svg")
      .attr("width", width)
      .attr("height", height);

  var color = d3.scaleOrdinal(d3.schemeCategory20);

  var manybody = d3.forceManyBody().strength([-600]);

  var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.id; }))
      .force("charge", manybody)
      .force("center", d3.forceCenter(width / 2, height / 3));
      

  var link = svg.selectAll(".links")
      .data(graph.links)
      .enter().append("g")
      .attr("class", "links");


  var node = svg.selectAll(".node")
          .data(graph.nodes)
          .enter().append('g')
          .attr("class","nodes")
          .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

    // Filter large networks
    var link_limiter = 200;
    link.sort(function(a,b){
      return d3.descending(a.value[emotion_dict[current_emotion].name],b.value[emotion_dict[current_emotion].name])});
    link = link.filter(function(d,i){return i < link_limiter;});
    // end experimental filter

    // Filters the node that have 0 outgoing and incoming edges
    node.each(function(d) {
        d.inDegree = 0;
        d.outDegree = 0;
    });

    link.each(function(d) {
      if(d.value[emotion_dict[current_emotion].name] > 0){
          node.each(function(l){
          if(l.id == d.source){
              l.outDegree += 1;
          }
          if(l.id == d.target){
                    l.inDegree += 1;
                  }

                });
              }});

      node = node.filter(function(d){
        return d.outDegree > 0 || d.inDegree >  0;
      });
      
      link = link.filter(function(l){
        return l.value[emotion_dict[current_emotion].name] > 0;
      });
    // end filter


    // Constant line width
    var max_value = get_max(link);
    var min_value = get_min(link);

    function get_max(link){
      var max = 0;
      link.each(function(l){
        if(l.value[emotion_dict[current_emotion].name] > max){
          max = l.value[emotion_dict[current_emotion].name];
        }
      })
      return max;
    }

    function get_min(link){
      var min = Infinity;
      link.each(function(l){
        if(l.value[emotion_dict[current_emotion].name] < min){
          min = l.value[emotion_dict[current_emotion].name]
        }
      })
      return min;
    }
    
    var line_scale = d3.scaleLinear().domain([min_value,max_value]).range([1,10]);


    // Append circles, lines and labels
    var circle = node.append('circle')
              .attr('r',radius)
              .attr("fill", function(d) { return color(d.group); });
    
    var label = node.append('text')
        .text(function(d){return d.id;})
        .attr('dy',".35em")
        .style('font-size',"11px");

     var line = link.append('line')
            .attr("stroke-width", function(d) { 
        for(var i = 0;i <10; i++){
          if(emotion[i] == true){
            current_emotion = i.toString();
            break;
          }
        }
        if(current_emotion == null){current_emotion = "null";}
        return line_scale(d.value[emotion_dict[current_emotion].name]); })
      .style('stroke',function(){
        return emotion_dict[current_emotion].color;
      });

    // Hightlights connected nodes
    var toggle = 0;
    var linkedByIndex = {};
    
        node.each(function(d){
          linkedByIndex[d.id + "," + d.id] = 1;
        })

        link.each(function (l) {
          var s,t;
          node.each(function(d){
            if(d.id == l.source){

              s = d.id;
            }
            if(d.id == l.target){
              t = d.id;
            }
            
          })
          linkedByIndex[s + "," + t] = 1;});

        function neighboring(a, b) {
          return linkedByIndex[a.id + "," + b.id];
        }

    function connectedNodes() {
       
      if (toggle == 0) {
          //Reduce the opacity of all but the neighbouring nodes
          d = d3.select(this).node().__data__;
          node.style("opacity", function (o) {
              
              return neighboring(d, o) | neighboring(o, d) ? 1 : 0.2;
          });
          link.style("opacity", function (o) {

              return d.id==o.source.id | d.id==o.target.id ? 1 : 0.2;
          });
          circle.transition().attr("r",function(o){
            return o.id == d.id?radius + 6:radius;})
          .attr("fill",function(o){ return o.id==d.id?"forestgreen":color(d.group);});

          label.transition().style('font-size',
            function(o){ return o.id==d.id?"15px":"11px";});

          toggle = 1;

      } else {
          //Put them back to starting opacity
          node.style("opacity", 1);
          link.style("opacity", 0.8);
          circle.transition().attr('r',radius)
                    .attr("fill", function(d) { return color(d.group); });
          label.transition().style('font-size',"11px");
          toggle = 0;
      }
    }
    
    node.on('click', connectedNodes);
    // end function


  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);
      
  simulation.force("link")
      .links(graph.links);
    

  function ticked() {
    var padding = 50;
    line
        .attr("x1", function(d) { return d.source.x = Math.max(radius, Math.min(width - radius - padding, d.source.x)); })
        .attr("y1", function(d) { return d.source.y = Math.max(radius, Math.min(height - radius - padding, d.source.y)); })        
        .attr("x2", function(d) { return d.target.x = Math.max(radius, Math.min(width - radius - padding,d.target.x)); })
        .attr("y2", function(d) { return d.target.y = Math.max(radius, Math.min(height - radius - padding, d.target.y)); });
        
    circle
        .attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius - padding, d.x)); })
        .attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius - padding, d.y)); });
    
    label
        .attr('x',function(d){return d.x;})
        .attr('y',function(d){return d.y;});

  }

  // Functions for dragging
  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
  // end functions for dragging  
}
