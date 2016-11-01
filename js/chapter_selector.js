function networkcall(mainsvg){
  // chapter selector

  var chapter = new Array(9);
  for(var i = 0;i < chapter.length; i++){
      chapter[i] = false;
    }

  chapter[0] = true;
  // end chapter selector

  // emotion selector
  var emotion_dict = {
    "0": {"name":"Anticipation","color":""},
    "1": {"name":"Sadness","color":""},
    "2": {"name":"Disgust","color":""},
    "3": {"name":"Joy","color":""},
    "4": {"name":"Anger","color":""},
    "5": {"name":"Surprise","color":"blue"},
    "6": {"name":"Fear","color":"orange"},
    "7": {"name":"Trust","color":""},
    "8": {"name":"Positive","color":""},
    "9": {"name":"Negative","color":""},
    "null": {"name":"Count","color":"#999"}
  };

  var emotion = new Array(10);
  for(var i = 0;i <10; i++){
    emotion[i] = false;
  }
  //emotion[0] = true;
  //emotion[1] = true;

  var current_emotion = null;
  // end emotion selector

  function force_call(){
    // create data
    d3.json("../Data/second.json", function(error, graph) {
      if (error) throw error;

      data = graph["force_list"];

      var nodes_list = [];
      var links_list = [];
      var links_set = new Set();

      for(var i = 0;i < chapter.length; i++){
        if(chapter[i] == true){
          // dictionary 
          var current_data = data[i];
          
          // list of nodes
          var current_node = current_data["nodes"];
          for(var j = 0; j < current_node.length; j++){
            var node = current_node[j];
            // check if contains
            var flag = false;
            for(var z = 0; z < nodes_list.length; z++){
              var cur = nodes_list[z];
              if(cur["id"] == node["id"]){
                flag = true;
              }
            }
            // if no nodes match append it
            if(flag == false){
              nodes_list.push(node);
            }
          }
          
          // list of links
          var current_link = current_data["links"];
          for(var j = 0; j < current_link.length; j++){
            var link = current_link[j];
            var a = link["source"];
            var b = link["target"];
            var val = link["value"];
            var flag = false;
            // check the entire list for copies
            for(var k = 0; k < links_list.length; k++){
              var l = links_list[k];
              // if match add values
              if((a == l["source"] && b == l["target"]) || ( b == l["source"] && a == l["target"])){
                var key_list = Object.keys(l["value"]);
                for(var x = 0; x < key_list.length;x++){
                  var key = key_list[x];
                  // add keys
                  l["value"][key] += val[key];
                  flag = true;
                  break;
                }
              }
            }
      
            // if not present append it
            if(flag == false){
              links_list.push({"source" : a, "target" : b, "value" : val});
            }
          }
        }
      }

      data = {"nodes" : nodes_list, "links" : links_list};
      force(data,emotion_dict,current_emotion,emotion);
    });  
  }
  force_call();  
}

