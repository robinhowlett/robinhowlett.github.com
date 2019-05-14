var driver = new SankeyDriver();
d3.json('/assets/data/wager-data.json', function(wagerData){
  var margin = {
    top: 0, bottom: 10, left: 0, right: 10,
  };
  var size = {
    width: 800, height: 480,
  }
  driver.prepare(d3.select("#canvas"), size, margin);
  driver.draw(wagerData);
  sendBeacon("sankey.draw");
});