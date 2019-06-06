var socket = io.connect('http://' + document.domain + ":" + location.port);
var timer = document.getElementById('timer');
var canvas = document.getElementById('drawingCanvas');
var ctx = canvas.getContext('2d');
var clearbtn = document.getElementById('clearbtn');
var paintbtn = document.getElementById('paint');
var penbtn = document.getElementById('pen');
var wordSelection = document.getElementById('wordSelection');
var scoreboard = document.getElementById('scoreboard');
var isCurrDrawer = false;

var scores = {};
var isDrawing = false;
var drawMode = 'pen';
var prevX = 0;
var prevY = 0;
var lineWidth = 3;
var prevDrawer = null;

wordSelection.style.display = 'none'; // Default no word selection shown

// Set canvas background to opaque white
ctx.fillStyle = 'rgba(255,255,255,1)';
ctx.fillRect(0, 0, canvas.width, canvas.height);

// Eliminate non opaque pixels
ctx.filter = 'url(#remove-alpha)';

var cursorStyle = document.createElement('style');
document.head.appendChild(cursorStyle);

var msgbox = document.getElementById('msg');
//var msgform = document.getElementById('chatform')

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
///*
var clrWheel = d3.select("#clrwheel")
                 .append("svg")
                 .attr("width", 150)
                 .attr("height", 150)
//*/
//var clrWheel = document.getElementById("clrwheel")
//console.log(clrWheel)
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
var clrSelect = d3.select("#clrwheel")
                  .append("svg")
                  .attr("width", 500)
                  .attr("height", 500)


var colorList = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "black"]
var count = 0
for (var j = 0; j < colorList.length; j++){
  if (j % 4 == 0){
    var xxx = 10 + (30 * 4)
    var yyy = 10 + (30 * (count ))
    clrSelect.append("rect")
              .attr("x", xxx)
              .attr("y", yyy)
              .attr("width", 60)
              .attr("height", 30)
              .attr("fill", "white")
              .on("click",function(){
                newC = this.getAttribute("fill")
                console.log(newC)
                color = newC
                //console.log(see)
                //see.setAttribute("fill", newC)
              })
    count = count + 1
  }
  clrSelect.append("rect")
            .attr("x", 10 + (30 * (j % 4)))
            .attr("y", 10 + (30 * (count - 1)))
            .attr("width", 30)
            .attr("height", 30)
            .attr("fill", colorList[j])
            .on("click",function(){
              newC = this.getAttribute("fill")
              console.log(newC)
              color = newC
              //console.log(see)
              //see.setAttribute("fill", newC)
            })
  }
  clrSelect.append("line")
          .attr("x1", 10 + (30 * 6))
          .attr("y1", 10)
          .attr("x2", 10 + (30 * 6))
          .attr("y2", 10 + 60)
          .attr("stroke", "black")
  clrSelect.append("line")
          .attr("x1", 10)
          .attr("y1", 10 + 60)
          .attr("x2", 10 + (30 * 6))
          .attr("y2", 10 + 60)
          .attr("stroke", "black")
  clrSelect.append("line")
          .attr("x1", 10)
          .attr("y1", 10)
          .attr("x2", 10 + (30 * 6))
          .attr("y2", 10)
          .attr("stroke", "black")
  clrSelect.append("line")
          .attr("x1", 10)
          .attr("y1", 10)
          .attr("x2", 10)
          .attr("y2", 10 + 60)
          .attr("stroke", "black")

//================================================

ctx.lineCap = 'round';

var equalColor = function(startColor, lookupPos, imgData) {
  //Get RGB values of the current pixel
  var r = imgData.data[lookupPos];
  var g = imgData.data[lookupPos + 1];
  var b = imgData.data[lookupPos + 2];
  //Compare to the starting pixel and return the result
  return r == startColor[0] && g == startColor[1] && b == startColor[2];
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
  var sendColor = fillColor;
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
    socket.emit('newLine', ['p', x, y, sendColor]);
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

var chooseWord = function(index) {
  socket.emit('chooseWord', index);
}

var clearBoard = function(sendBack = true) {
  ctx.fillStyle = 'rgba(255,255,255,1)';
  ctx.fillRect(0,0,canvas.width,canvas.height); //Clears the entire canvas
  if (sendBack) {
    socket.emit('clearBoard', null);
  }
}

var setPen = function() {
  drawMode = 'pen';
}

var setPaint = function() {
  drawMode = 'fill';
}

var addtoScoreboard = function(playerName) {
  var newRow = document.createElement('div');
  newRow.className = 'row';
  var nameDisp = document.createElement('div');
  nameDisp.className = 'col-sm-8';
  nameDisp.innerHTML = playerName;
  var scoreDisp = document.createElement('div');
  scoreDisp.className = 'col-sm-4';
  scoreDisp.innerHTML = 0;
  newRow.appendChild(nameDisp);
  newRow.appendChild(scoreDisp);
  scoreboard.append(newRow);
  scores[playerName] = [scoreDisp, newRow];
}

socket.on('connect', function() { //Executed upon opening the site
  var params = (new URL(document.location)).searchParams;
  var roomID = params.get('roomID');
  if (roomID == null || roomID == '') { //Defaults room if user joins without specifying a roomID
    roomID = 'Default';
  }
  socket.emit('joinRoom', roomID); //Join room specified by roomID parameter
  console.log('Successfully Connected to ' + roomID);
  socket.emit('requestLines', null);
});

socket.on('highlightDrawer', function(drawer) {
  console.log(drawer + ' is Drawing');
  if (prevDrawer != null) {
    scores[prevDrawer][1].className = 'row';
  }
  prevDrawer = drawer;
  console.log(scores);
  scores[drawer][1].className = 'row border border-primary';
});

socket.on('yourturn', function(data) {
  wordSelection.children[0].innerHTML = data[0];
  wordSelection.children[1].innerHTML = data[1];
  wordSelection.children[2].innerHTML = data[2];
  wordSelection.style.display = 'block';
  console.log(data);
});

socket.on('startDrawing', function(data) {
  isCurrDrawer = true;
  wordSelection.style.display = 'none';
});

socket.on('notyourturn', function(data) {
  isCurrDrawer = false;
});

socket.on('recieveLines', function(lines) {
  for (var i = 0; i < lines.length; i += 1) {
    currLine = lines[i];
    drawLine(currLine[0], currLine[1], currLine[2], currLine[3], currLine[5], sendBack = false, inputWidth = currLine[4]);
  }
});

socket.on('newLine', function(line) {
  console.log(line);
  if (line[0] == 'p') {
    fill(line[1], line[2], line[3], sendBack = false);
  }
  drawLine(line[0], line[1], line[2], line[3], line[5], sendBack = false, inputWidth = line[4]);
});

socket.on('clearBoard', function(data) {
  clearBoard(sendBack = false);
});

socket.on('newPlayer', function(playerName) {
  addtoScoreboard(playerName);
});

socket.on('playerLeave', function(playerName) {
  scoreboard.removeChild(scores[playerName][1]);
  delete scores[playerName];
});

socket.on('updateScores', function(newScores) {
  console.log(newScores);
  var keys = Object.keys(newScores);
  for (var i = 0; i < keys.length; i++) {
    var currKey = keys[i];
    if (!(currKey in scores)) { //Add to scoreboard if the player is not already there
      addtoScoreboard(currKey);
    }
    scores[currKey][0].innerHTML = newScores[currKey];
  }
});

socket.on('updateTimer', function(newTime) {
  timer.innerHTML = newTime;
});

clearbtn.addEventListener('click', function(e) {
  if (isCurrDrawer) {
    clearBoard();
  }
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
  newMsg.innerHTML = msg;
  chatlog.appendChild(newMsg);
  chatlog.scrollTop = chatlog.scrollHeight;
});

msgbox.addEventListener("keydown", function(e){
  if (e.keyCode == 13){ //Check for enter key press
    e.preventDefault();
    sendMessage();
  }
});

var sendbutton = document.getElementById("send");

sendbutton.addEventListener("click", function(e){
  e.preventDefault();
  sendMessage();
});

var picurl = canvas.toDataURL()
console.log(picurl)
