var socket = io.connect('http://' + document.domain + ":" + location.port);
var timer = document.getElementById('timer');
var canvas = document.getElementById('drawingCanvas');
var ctx = canvas.getContext('2d');
var clearbtn = document.getElementById('clearbtn');
var paintbtn = document.getElementById('paint');
var penbtn = document.getElementById('pen');
var isCurrDrawer = false;
var fillTolerance = 25;

var isDrawing = false;
var drawMode = 'pen';
//var prevX = 0;
//var prevY = 0;
//var lineWidth = 3;

ctx.fillStyle = 'rgba(255,255,255,1)';
ctx.fillRect(0, 0, canvas.width, canvas.height);

var cursorStyle = document.createElement('style');
document.head.appendChild(cursorStyle);

var msgbox = document.getElementById('msg');
//var msgform = document.getElementById('chatform')

var picurl = canvas.toDataURL()

var drawLine = function(x0, y0, x1, y1, lineColor, sendBack = true, inputWidth = lineWidth) {
  ctx.lineWidth = inputWidth;
  ctx.beginPath();
  ctx.moveTo(x0, y0); //Offset x and y by vector
  ctx.lineTo(x1, y1); //Draw line to center of the next circle
  ctx.strokeStyle = lineColor
  ctx.stroke();
};

/*
// Set canvas background to opaque white
ctx.fillStyle = 'rgba(255,255,255,1)';
ctx.fillRect(0, 0, canvas.width, canvas.height);

var cursorStyle = document.createElement('style');
document.head.appendChild(cursorStyle);

var msgbox = document.getElementById('msg');
//var msgform = document.getElementById('chatform')
*/
//================= color wheel ==================
var color = 'rgba(0,0,0,1)';
var oldcolor = 'rgba(0,0,0,1)';

var distance = function(x0,y0,x1,y1){
  var dx = Math.pow(Math.abs(x0 - x1), 2)
  var dy = Math.pow(Math.abs(y0 - y1), 2)
  return Math.pow(dx + dy, 0.5)
}

var hsv_to_rbg = function(h, s, v){
  if (h >= 360 || s * v == 0 || s > 1 || v > 1){
    return [0, 0, 0]
  }
  var c = v * s
  var x = c * (1 - Math.abs((h/60) % 2 - 1))
  var m = v - c
  var rbg = [0,0,0]
  if (h < 60){
    rbg = [c,x,0]
  }
  else if (h < 120) {
    rbg = [x,c,0]
  }
  else if (h < 180) {
    rbg = [0,c,x]
  }
  else if (h < 240) {
    rbg = [0,x,c]
  }
  else if (h < 300) {
    rbg = [x,0,c]
  }
  else {
    rbg = [c,0,x]
  }
  for (var u = 0; u < 3; u++){
    var new_val = (rbg[u] + m) * 255
    if (new_val % 1 < 0.5){
      rbg[u] = Math.floor(new_val)
    }
    else{
      rbg[u] = Math.ceil(new_val)
    }
  }
  return rbg
}
//var colorData = []

var center = [75,75]
var max_rad = 70
//var clrWheel = document.getElementById("clrWheel")
var clrWheel = d3.select("body")
                 .append("svg")
                 .attr("width", 150)
                 .attr("height", 150)
var colorWheel = function(){
  for (var i = 0; i < 150; i++){
    //var temp = []
    for (var j = 0; j < 150; j++){
      var dist = distance(i, j, center[0], center[1])
      if (dist <= max_rad){
        var theta = Math.atan2(i - max_rad,j - max_rad) * ( 180.0 / Math.PI)
        if (theta < 0){
          theta = 360 + theta
        }
        //console.log("theta")
        //console.log(theta)
        var hsvChanged = hsv_to_rbg(theta , dist / max_rad, 1)
        ///*
        clrWheel.append("rect")
                .attr("x", j)
                .attr("y", i)
                .attr("height", 1)
                .attr("width", 1)
                .attr("fill", rgb(hsvChanged))
                .attr("rgbval", 'rgba(' + hsvChanged.join() + ',1)')
                .on("click",function(){
                  //console.log(hsvChanged)
                  newC = this.getAttribute("rgbval")
                  console.log(newC)
                  color = newC
                })
        //*/
        //temp.append(rgb(hsvChanged))
      }
    }
    //colorData.append(temp)
  }
}

function rgb(color){
    //console.log(color)
    temp="#"
    for (var i=0; i<color.length;i++){
      var hex = color[i].toString(16);
      hex.length == 1 ? "0" + hex : hex;
      temp+=hex
    }
    return temp
}


colorWheel()
//console.log(colorData)
//================================================
/*
ctx.lineCap = 'round';

var equalColor = function(startColor, lookupPos, imgData) {
  //Get RGB values of the current pixel
  var dr = (imgData.data[lookupPos] - startColor[0]) ** 2;
  var dg = (imgData.data[lookupPos + 1] - startColor[1]) ** 2;
  var db = (imgData.data[lookupPos + 2] - startColor[2]) ** 2;
  //Compare to the starting pixel and return the result
  return (dr + dg + db < fillTolerance);
}

var setColor = function(pixelPos, color, imgData) {
  imgData.data[pixelPos] = color[0];
  imgData.data[pixelPos + 1] = color[1];
  imgData.data[pixelPos + 2] = color[2];
  // imgData.data[pixelPos + 3] = 255;
}

var fill = function(x, y, fillColor, sendBack = true) {
  // var printCount = 100;
  // console.log('fillColor:');
  console.log(fillColor);
  var pixelStack = [[x,y]];
  var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  var currPos = (x + (y * canvas.width)) * 4;
  var startColor = imgData.data.slice(currPos, currPos + 3);
  // console.log('startColor:');
  // console.log('rgba(' + startColor.join() + ',1)');
  ctx.fillStyle = fillColor;
  fillColor = fillColor.substring(5, fillColor.length - 3).split(',');
  for (var index = 0; index++; index < 3) {
    // console.log(fillColor);
    fillColor[index] = parseInt(fillColor[index]);
  }
  if ( equalColor(fillColor, currPos, imgData) ) { //Exit if filling an area of the same color
    console.log('same');
    return;
  }

  while (pixelStack.length != 0) {
    var currPixel = pixelStack.pop();
    x = currPixel[0];
    y = currPixel[1];
    currPos = (x + (y * canvas.width)) * 4;

    //Go up until a non matching color is reached
    while (y >= 0 && equalColor(startColor, currPos, imgData)) {
      y -= 1;
      currPos -= canvas.width * 4;
    }
    //Correct shooting over by one pixel
    y += 1;
    currPos += canvas.width * 4;

    //Start going down
    while (y < canvas.height && equalColor(startColor, currPos, imgData)) {
      setColor(currPos, fillColor, imgData);
      leftChange = true;
      rightChange = true;

      //Check on left pixel
      if (x > 0 && leftChange && equalColor(startColor, currPos - 4, imgData)) {
        pixelStack.push([x - 1, y]);
        leftChange = false;
      } else {
        leftChange = true;
      }
      //Check on right pixel
      if (x < canvas.width - 1 && rightChange && equalColor(startColor, currPos + 4, imgData)) {
        pixelStack.push([x + 1, y]);
        // if (printCount > 0) {
        //   console.log([x + 1, y]);
        //   printCount -= 1;
        // }
        rightChange = false;
      } else {
        rightChange = true;
      }

      //Move down
      y += 1;
      currPos += canvas.width * 4;
    }
  }
  //Update image data
  ctx.putImageData(imgData, 0, 0);

  if (sendBack) {
    console.log('Send paint attempted');
    // socket.emit('newLine', [x, y, fillColor]);
  }
}

var drawLine = function(x0, y0, x1, y1, lineColor, sendBack = true, inputWidth = lineWidth) {
  ctx.lineWidth = inputWidth;
  ctx.beginPath();
  ctx.moveTo(x0, y0); //Offset x and y by vector
  ctx.lineTo(x1, y1); //Draw line to center of the next circle
  ctx.strokeStyle = lineColor
  ctx.stroke();
  if (sendBack) {
    socket.emit('newLine', [x0, y0, x1, y1, inputWidth, color]);
  }
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

var clearBoard = function(sendBack = true) {
  ctx.fillStyle = 'rgba(255,255,255,1)';
  ctx.fillRect(0,0,canvas.width,canvas.height); //Clears the entire canvas
  if (sendBack) {
    socket.emit('clearBoard', null);
  }
}

socket.on('connect', function() { //Executed upon opening the site
  console.log('Successfully Connected');
  socket.emit('joinRoom', 'General'); //Automatically join General
  socket.emit('requestLines', null);
});

socket.on('yourturn', function(data) {
  isCurrDrawer = true;
});

socket.on('notyourturn', function(data) {
  isCurrDrawer = false;
});
/*
socket.on('recieveLines', function(lines) {
  for (var i = 0; i < lines.length; i += 1) {
    currLine = lines[i];
    drawLine(currLine[0], currLine[1], currLine[2], currLine[3], currLine[5], sendBack = false, inputWidth = currLine[4]);
  }
});

socket.on('newLine', function(line) {
  // console.log(line);
  drawLine(line[0], line[1], line[2], line[3], line[5], sendBack = false, inputWidth = line[4]);
});
*/
socket.on('clearBoard', function(data) {
  clearBoard(sendBack = false);
});

socket.on('updateTimer', function(newTime) {
  timer.innerHTML = newTime;
});

canvas.addEventListener('mousedown', function(e) {
  if (isCurrDrawer) {
    if (drawMode == 'pen') {
      prevX = e.offsetX;
      prevY = e.offsetY;
      isDrawing = true;
      drawLine(prevX, prevY, prevX, prevY, color);
    } else if (drawMode == 'fill') {
      fill(e.offsetX, e.offsetY, color);
    }
  }
});

canvas.addEventListener('mousemove', function(e) {
  if (isCurrDrawer && isDrawing && drawMode == 'pen') {
    //Draw the line
    drawLine(prevX, prevY, e.offsetX, e.offsetY, color);
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
*/
/*
socket.on('chat', function(msg){
  var msg = document.getElementById("message");
  console.log(msg);
  msgbox.append("<div>"+msg+"</div>")
});

msgform.addEventListener("submit", function(e){
  e.preventDefault();
  var msg = document.getElementById("message");
  console.log(msg)
  send(msg)
});
*/
/*
socket.on("message", function(msg){
  var msg = document.getElementById("message")
  msgbox.append("<li>"+ msg +"</li>");
  console.log("recieved msg");

});
*/
var sendMessage = function() {
  console.log("Sending message");
  var newMsg = msgbox.value;
  socket.send(newMsg);
  msgbox.value = "";
}

socket.on("message", function(msg){
  var chatlog = document.getElementById('chatlog');
  var newMsg = document.createElement('li');
  var children = chatlog.children;
  if (children.length > 10) {
    chatlog.removeChild(children[0]);
  }
  newMsg.innerHTML = msg;
  chatlog.appendChild(newMsg)
});

msgbox.addEventListener("keydown", function(e){
  if (e.keyCode == 13){
    e.preventDefault();
    sendMessage();
  }
});

var sendbutton = document.getElementById("send");

sendbutton.addEventListener("click", function(e){
  e.preventDefault();
  sendMessage();
});
