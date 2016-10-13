<<<<<<< HEAD
// declares a tree layout and assigns the size
var treemap = d3.tree()
    .size([360, 400])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

var randomvalues = {}

=======
<<<<<<< HEAD
// declares a tree layout and assigns the size
var treemap = d3.tree()
    .size([360, 300])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 0.5) / a.depth; });

// load the external data
d3.json("../Mod_data.json", function(error, treeData) {
  if (error) throw error;

  //  assigns the data to a hierarchy using parent-child relationships
  var nodes = d3.hierarchy(treeData, function(d) {
    return d.children;
    });

  // maps the node data to the tree layout
  nodes = treemap(nodes);

  // append the svg object to the body of the page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin

  // adds the links between the nodes

  var val = []
  for (var i = 0; i < 100 ; i++)
  {
    val.push(Math.random() * 75);
  }

  i = 0;

  var link = g.selectAll(".link")
      .data(nodes.descendants().slice(1))
      .enter().append("path")
      .attr("class", "link")
      .attr("d", function(d) {
        //if(d.depth == 2){
          if(d.x >= 0 & d.x < 90){
            d.y += val[i++] + 50;
          }
          else if (d.x >= 90 & d.x <180){
            d.y += val[i++] + 100;
          }
          else if (d.x >= 180 & d.x < 270){
            d.y += val[i++];
          }
          else{
            d.y += val[i++] + 150;
          }
        //}
        return "M" + project(d.x, d.y)
            + "L " + project(d.parent.x, d.parent.y)})
        .attr("stroke", "mistyrose")
        .attr("stroke-width", 1);
      
  i = 0;    
  // adds each node as a group
  var node = g.selectAll(".node")
      .data(nodes.descendants())
      .enter().append("g")
      .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
      .attr("transform", function(d) {
        //d.y += val[i++]; 
        return "translate(" + project(d.x, d.y) + ")"; });

  // adds the circle to the node
  node.append("circle")
      .attr("r", 1);

  // adds the text to the node
});

function project(x, y) {
  var angle = (x - 90) / 180 * Math.PI, radius = y;
  return [radius * Math.cos(angle), radius * Math.sin(angle)];
}
=======
// declares a tree layout and assigns the size
var treemap = d3.tree()
    .size([360, 300])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

>>>>>>> origin/master
// load the external data
d3.json("Data/modfinaldata.json", function(error, treeData) {
  if (error) throw error;

  //  assigns the data to a hierarchy using parent-child relationships
  var nodes = d3.hierarchy(treeData, function(d) {
    return d.children;
    });

  // maps the node data to the tree layout
  nodes = treemap(nodes);

  // append the svg object to the body of the page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin

  // adds the links between the nodes
  var link = g.selectAll(".link")
      .data(nodes.descendants().slice(1))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", function(d) {
<<<<<<< HEAD
          if(d.depth==2){
             randomvalues[d.name]=(Math.random()*150);
             d.y = d.y + 20 - randomvalues[d.name];  
          }
        return "M" + project(d.x, d.y)
            + "L " + project(d.parent.x, d.parent.y)})
        .attr("stroke", function(d){
          if(d.depth==3){
          if(d.data.sentiment == "pos"){return "#green";}
          else if(d.data.sentiment == "neg"){return "#red";}
=======
        return "M" + project(d.x, d.y)
            + "L " + project(d.parent.x, d.parent.y)})
        .attr("stroke", function(d){
          console.log(d);
          if(d.data.sentiment == "pos"){return "green";}
          else if(d.data.sentiment == "neg"){return "red";}
>>>>>>> origin/master
          else{
            if(d.depth==3){
              return "#yellow";}
            else{
<<<<<<< HEAD
              return "#aaa";
            }}
        }
         else if(d.depth==2){
             if(d.data.sentiment < 0){
                 return "#d00";
             }
             else if(d.data.sentiment > 0){
                 return "#2b8cbe";
             }
             else{
                 return "#gray";
             }
         }
        else{
            return "#999"
        }
        })
        .attr("stroke-width", 0.8)
=======
              return "#999"
            }
            }
        })
        .attr("stroke-width", 1)
>>>>>>> origin/master
        .attr("opacity",function(d){
          if(d.depth==2){
              return 0.4;}
            else{
              return 1;}
          });
      
    
  // adds each node as a group
  var node = g.selectAll(".node")
      .data(nodes.descendants())
    .enter().append("g")
      .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
<<<<<<< HEAD
      .attr("transform", function(d) { return "translate(" + project(d.x, (d.children?d.y:d.y+randomvalues[d.parent])) + ")"; });

  // adds the circle to the node
  node.append("circle")
      .attr("r", function(d){
      if((d.depth==2)&(d.data.sentiment==0))
          return 0;
      else
          return 0.2;
  });
=======
      .attr("transform", function(d) { return "translate(" + project(d.x, d.y) + ")"; });

  // adds the circle to the node
  node.append("circle")
      .attr("r", 0.1);
>>>>>>> origin/master

  // adds the text to the node
  
    
});

function project(x, y) {
  var angle = (x - 90) / 180 * Math.PI, radius = y;
  return [radius * Math.cos(angle), radius * Math.sin(angle)];
}
<<<<<<< HEAD
=======
>>>>>>> 3bfdb61e30e3f9d10e6a3fce8f5ae0b3a05827b4
>>>>>>> origin/master
