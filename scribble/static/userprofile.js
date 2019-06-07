var canvas = document.getElementById('drawingCanvas');
var ctx = canvas.getContext('2d');
var clearbtn = document.getElementById('clearbtn');
var finishbtn = document.getElementById('finishbtn');
var pictext = document.getElementById('pic');

var isDrawing = false;
var prevX = 0;
var prevY = 0;
var lineWidth = 3;

var cursorStyle = document.createElement('style');
document.head.appendChild(cursorStyle);

ctx.lineCap = 'round';

var drawLine = function(x0, y0, x1, y1, inputWidth = lineWidth) {
  ctx.lineWidth = inputWidth;
  ctx.beginPath();
  ctx.moveTo(x0, y0); //Offset x and y by vector
  ctx.lineTo(x1, y1); //Draw line to center of the next circle
  ctx.stroke();

}

var changeCursor = function() {
  let newCursor = `cursor: url('data:image/svg+xml;utf8,\
    <svg id="svg" xmlns="http://www.w3.org/2000/svg" version="1.1" width="32" height="32">\
      <circle cx="12.5" cy="12.5" r="${lineWidth / 2 + 1}" fill-opacity="0" style="stroke: black;"/>\
      <circle cx="12.5" cy="12.5" r="${lineWidth / 2}" fill-opacity="0" style="stroke: white;"/>\
    </svg>')
  12.5 12.5, pointer;`
  cursorStyle.innerHTML = `#drawingCanvas { ${newCursor} }`;
}

var clearBoard = function() {
  ctx.clearRect(0,0,canvas.width,canvas.height); //Clears the entire canvas
}

canvas.addEventListener('mousedown', function(e) {
  prevX = e.offsetX;
  prevY = e.offsetY;
  isDrawing = true;
  drawLine(prevX, prevY, prevX, prevY);
});

canvas.addEventListener('mousemove', function(e) {
  if (isDrawing) {
    //Draw the line
    drawLine(prevX, prevY, e.offsetX, e.offsetY);
    prevX = e.offsetX;
    prevY = e.offsetY;
  }
});

canvas.addEventListener('mouseout', function(e) {
  isDrawing = false;
});

canvas.addEventListener('mouseup', function(e) {
  isDrawing = false;
});

var finishdrawing = function(e) {
  var picurl = canvas.toDataURL();
  pictext.value = picurl;
  return picurl;
};

finishbtn.addEventListener('click', function(e){
  isDrawing = false;
  finishdrawing();
  console.log(finishdrawing());
});

canvas.addEventListener("wheel", function(e) {
  var change;
  if (e.deltaY > 0) {
    change = -1;
  } else {
    change = 1;
  }
  lineWidth += change;
  //console.log(lineWidth);
  if (lineWidth < 3) { //Clamp min brush size to 3 pixels
    lineWidth = 3;
  } else if (lineWidth > 20) { //Clamp max brush size to 20 pixels
    lineWidth = 20;
  }
  changeCursor();
  e.preventDefault(); //Prevent user from scrolling down the page
});

changeCursor();