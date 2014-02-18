function fetchBibleVerse() {
  var response;
  var req = new XMLHttpRequest();
  // build the GET request
  req.open('GET', "http://www.ourmanna.com/verses/api/get/?format=text&order=random", true);
  req.onload = function(e) {
    if (req.readyState == 4) {
      // 200 - HTTP OK
      if(req.status == 200) {
        console.log(req.responseText);
        Pebble.sendAppMessage({
            "verse": req.responseText});
      } else {
        console.log("Request returned error code " + req.status.toString());
        Pebble.sendAppMessage({
            "verse": "Request returned error code " + req.status.toString()});
      }
    }
  }
  req.send(null);
}

// Set callback for the app ready event
Pebble.addEventListener("ready",
                        function(e) {
                          console.log("connect!" + e.ready);
                          console.log(e.type);
                          fetchBibleVerse();
                        });

