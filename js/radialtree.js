
// declares a tree layout and assigns the size
var treemap = d3.tree()
    .size([360, 300])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

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
        return "M" + project(d.x, d.y)
            + "L " + project(d.parent.x, d.parent.y)})
        .attr("stroke", function(d){
          if(d.data.sentiment == "pos"){return "green";}
          else if(d.data.sentiment == "neg"){return "red";}
          else{
            if(d.depth==3){
              return "#yellow";}
            else{
              return "#999"
            }
            }
        })
        .attr("stroke-width", 1)
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
      .attr("transform", function(d) { return "translate(" + project(d.x, d.y) + ")"; });

  // adds the circle to the node
  node.append("circle")
      .attr("r", 0.1);

  // adds the text to the node
    
});

function project(x, y) {
  var angle = (x - 90) / 180 * Math.PI, radius = y;
  return [radius * Math.cos(angle), radius * Math.sin(angle)];
}

