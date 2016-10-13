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