var socket = io.connect('http://' + document.domain + ":" + location.port + '/lobby');
var roster = document.getElementById('roster');

var rosterdct = {};
var prevLeader = null;

var addToRoster = function(player) {
  var newPlayer = document.createElement('li');
  newPlayer.innerHTML = player;
  roster.appendChild(newPlayer);
  rosterdct[player] = newPlayer;
}

var createGame = function() {
  var output = {};
  var numRounds = document.getElementById('numRounds');
  var maxTime = document.getElementById('maxTime');
  maxTime = maxTime.options[maxTime.selectedIndex].value;
  numRounds = numRounds.options[numRounds.selectedIndex].value;
  output['maxTime'] = maxTime;
  output['numRounds'] = numRounds;
  socket.emit('createGame', output);
}

socket.on('newLeader', function(data) {
  if (prevLeader != null) {
    rosterdct[prevLeader].style.color = 'black';
  }
  console.log(data);
  rosterdct[data].style.color = 'gold';
});

socket.on('gameCreated', function() {
  window.location.href = 'http://' + document.domain + ":" + location.port + '/game' + window.location.search;
});

socket.on('connect', function() { //Executed upon opening the site
  var params = (new URL(document.location)).searchParams;
  var roomID = params.get('roomID');
  if (roomID == null || roomID == '') { //Defaults room if user joins without specifying a roomID
    roomID = 'Default';
  }
  // console.log(roomID);
  socket.emit('joinLobby', roomID); //Join room specified by roomID parameter
});

socket.on('updateRoster', function(data) {
  console.log(data);
  for (var i = 0; i < data.length; i++) {
    addToRoster(data[i]);
  }
});

socket.on('playerLeave', function(data) {
  roster.removeChild(rosterdct[data]);
  delete rosterdct[data];
});

socket.on('newPlayer', function(data) {
  addToRoster(data);
});
