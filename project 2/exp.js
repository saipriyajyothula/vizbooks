var units = "Widgets";

// set the dimensions and margins of the graph
var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 750 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom;

// format variables
var formatNumber = d3.format(",.0f"),    // zero decimal places
    format = function(d) { return formatNumber(d) + " " + units; },
    color = d3.scaleOrdinal(d3.schemeCategory20);

// append the svg object to the body of the page
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

// Set the sankey diagram properties
var sankey = d3.sankey()
    .nodeWidth(18)
    .nodePadding(20)
    .size([width, height]);

var path = sankey.link();


var generateData= function(){
  finaldata4={};
  d3.json('third.json',function(data) {
    var finaldata={}
    var resources = data.character_emotion;

    var chapter = new Array(9);
    for(var i = 0; i < 9; i++){
      chapter[i] = true;
    }
    for(var i=0;i<resources.length;i++)
    {
      var obj = resources[i];
      var name = obj.character_name;
      //finaldata["name"]=name;
      var chpdata = obj.chap_sentiment;
      all_val={}
      var emotion = ["Anticipation","Sadness","Disgust","Joy","Anger","Surprise","Fear","Trust","Total"];
      for (var j=0; j<emotion.length;j++){
        key=emotion[j];
        all_val[key] = 0;
      }
      for(var j = 0;j< chpdata.length; j++)
      {
        item=chpdata[j];
        if (true){
          if(item.value!=null)
          {
            for(var key in item.value){
              if(!(key=="Positive" || key=="Negative"||key=="Total"))
                all_val[key] = (+all_val[key]) + (+item.value[key]);
            }
          }
        }       
      }
      all_val['Total']= +0;
      for (var j=0; j<emotion.length;j++){
        key=emotion[j];
        if(key!="Total")
        {
          all_val["Total"]= (+all_val["Total"]) + (+all_val[key]);
        }
      }
      if(name!="Mr"&&name!="Mrs")
        finaldata[name]=all_val;
    }
    var finaldata2=[];
    for(var key in finaldata)
      finaldata2.push([key,finaldata[key]])

    finaldata2.sort(function(a,b){
      return +b[1]["Total"] - +a[1]["Total"];
    })


    var finaldata3=[];
    for(var j=0;j<10;j++)
      finaldata3.push(finaldata2[j]);

      sankeyData = finaldata4;
      console.log(Object.keys(sankeyData));

      // load the data
        sankey
            .nodes(sankeyData["nodes"])
            .links(sankeyData["links"])
            .layout(32);

      // add in the links
        var link = svg.append("g").selectAll(".link")
            .data(sankeyData["links"])
          .enter().append("path")
            .attr("class", "link")
            .attr("d", path)
            .style("stroke-width", function(d) { return Math.max(1, d.dy); })
            .sort(function(a, b) { return b.dy - a.dy; });

      // add the link titles
        link.append("title")
              .text(function(d) {
              return d.source.name + " → " + 
                      d.target.name + "\n" + format(d.value); });

      // add in the nodes
        var node = svg.append("g").selectAll(".node")
            .data(sankeyData["nodes"])
          .enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) { 
            return "translate(" + d.x + "," + d.y + ")"; })
            .call(d3.drag()
              .subject(function(d) {
                return d;
              })
              .on("start", function() {
                this.parentNode.appendChild(this);
              })
              .on("drag", dragmove));

      // add the rectangles for the nodes
        node.append("rect")
            .attr("height", function(d) { return d.dy; })
            .attr("width", sankey.nodeWidth())
            .style("fill", function(d) { 
            return d.color = color(d.name.replace(/ .*/, "")); })
            .style("stroke", function(d) { 
            return d3.rgb(d.color).darker(2); })
          .append("title")
            .text(function(d) { 
            return d.name + "\n" + format(d.value); });

      // add in the title for the nodes
        node.append("text")
            .attr("x", -6)
            .attr("y", function(d) { return d.dy / 2; })
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .attr("transform", null)
            .text(function(d) { return d.name; })
          .filter(function(d) { return d.x < width / 2; })
            .attr("x", 6 + sankey.nodeWidth())
            .attr("text-anchor", "start");

      // the function for moving the nodes
      function dragmove(d) {
          d3.select(this).attr("transform", 
              "translate(" + (
                  d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
              )
              + "," + (
                  d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
              ) + ")");
          sankey.relayout();
          link.attr("d", path);
        }}

  )};

generateData();