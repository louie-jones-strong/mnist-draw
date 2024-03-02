var model;

function ProcessImage(canvas) {
  // Convert on-screen image to something we can feed into our model.
  ctx = canvas.getContext('2d');
  const ctxScaled = document.getElementById('scaled-canvas').getContext('2d')
  ctxScaled.save();
  ctxScaled.clearRect(0, 0, ctxScaled.canvas.height, ctxScaled.canvas.width);
  ctxScaled.scale(28.0 / ctx.canvas.width, 28.0 / ctx.canvas.height)
  ctxScaled.drawImage(document.getElementById('canvas'), 0, 0)
  const {data} = ctxScaled.getImageData(0, 0, 28, 28)
  ctxScaled.restore();
  return document.getElementById('scaled-canvas')
}

// Canvas setup
var canvas = new fabric.Canvas('canvas');
canvas.isDrawingMode = true;
canvas.freeDrawingBrush.width = 25;
canvas.freeDrawingBrush.color = "#000000";
canvas.backgroundColor = "#ffffff";
canvas.renderAll();

// We don't want to do a prediction on every mouse move so we group
// the predictions according to the tuning variable movesPerPrediction.
var mouseMoveCount = 0;
var movesPerPrediction = 25;
var drawing = false;

function onMouseMove() {
  if (drawing && mouseMoveCount++ > movesPerPrediction) {
    canvas.freeDrawingBrush._finalizeAndAddPath();
    (async () => { Predict(); })();
    mouseMoveCount = 0;
  }
}

canvas.on('mouse:up',   () => {drawing = false; Predict();});
canvas.on('mouse:down', () => {drawing = true;});
canvas.on('mouse:move', onMouseMove);

// Clear button callback
$("#clear-canvas").click(function(){
  canvas.clear();
  canvas.backgroundColor = "#ffffff";
  canvas.renderAll();
  Predict();
  $("#status").removeClass();
});

var tensor_pixels = null;



// Initialize d3 bar chart
var labels = ['0','1','2','3','4','5','6','7','8','9'];
var zeros = [0,0,0,0,0,0,0,0,0,0,0];

var margin = {top: 0, right: 0, bottom: 20, left: 0},
    width = 360 - margin.left - margin.right,
    height = 180 - margin.top - margin.bottom;

var svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
       "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scale.ordinal()
          .rangeRoundBands([0, width], .1)
          .domain(labels);

var y = d3.scale.linear()
          .range([height, 0])
          .domain([0,1]);

var xAxis = d3.svg.axis()
              .scale(x)
              .orient("bottom")
              .tickSize(0);

svg.selectAll(".bar")
   .data(zeros)
   .enter().append("rect")
   .attr("class", "bar")
   .attr("x", function(d, i) { return x(i); })
   .attr("width", x.rangeBand())
   .attr("y", function(d) { return y(d); })
   .attr("height", function(d) { return height - y(d); });

svg.append("g")
   .attr("class", "x axis")
   .attr("transform", "translate(0," + height + ")")
   .call(xAxis);

// Update chart data
function updateChart(d) {
  d3.selectAll("rect")
    .data(d)
    .transition()
    .duration(300)
    .attr("y", function(d) { return y(d); })
    .attr("height", function(d) { return height - y(d); });
}



function Predict(){
  // Change status indicator
  $("#status").removeClass().toggleClass("fa fa-spinner fa-spin");

  let scaledCanvas = ProcessImage(canvas);

  var fac = (1.) / 1.;
  // var url = scaledCanvas.toDataURLWithMultiplier('png', fac);
  var url = scaledCanvas.toDataURL();


  // encode the image as png data url


  $.post('predict', url)
    .done(function (json) {
      if (json.result) {
        $("#status").removeClass().toggleClass("fa fa-check");
        $('#svg-chart').show();
        updateChart(json.data);

        // console.log('Prediction: ' + json.data.map(d => d.toFixed(2)))
      } else {
         $("#status").removeClass().toggleClass("fa fa-exclamation-triangle");
         console.log('Script Error: ' + json.error)
      }
    })
    .fail(function (xhr, textStatus, error) {
      console.log("POST Error: " + xhr.responseText + ", " + textStatus + ", " + error);
    }
  );



  // prediction = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0];
  // $("#status").removeClass().toggleClass("fa fa-check");
  // $('#svg-chart').show();
  // updateChart(prediction);
};


Predict();