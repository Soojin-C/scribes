from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash

import socket
import threading
import os
import random, string

from util import db_user as dbu
from util import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app, ping_interval = 1, ping_timeout = 5, allow_upgrades = False)

continueTimer = True
timerTime = 60 #Timer to be displayed
rooms = {} #request.sid : roomID
games = {} #roomID : game info dictionary
names = {} #request.sid : display name
#guessedCorrectly = set()


@app.before_first_request #Executed upon startup
def setup():
    try:
        dbu.build()
    except:
        pass
    countdown() #Start countdown timer

@app.route("/")
def root():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    #print(uuids)
    if dbu.son(uuids):
        return redirect(url_for("home"))
    return render_template("index.html", currTime = timerTime)

@app.route("/login")
def login():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/reg")
def reg():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/register", methods=["POST","GET"])
def regis():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        return redirect(url_for("home"))
    if request.method=="POST":
        user=request.form['user']
        try:
            use=dbu.suser(user)
        except:
            use=None
        if (use):
            flash("user exists")
            return redirect(url_for('reg'))
        pass1=request.form['pass']
        pass2=request.form['pass2']
        if len(pass1)>0 and len(user)>0:
            if pass1==pass2:
                dbu.auser(user,pass1)
                flash("user made")
                return render_template("index.html")
    flash("passwords do not match")
    return redirect(url_for('reg'))

#user=""
#friends=[]
@app.route("/auth", methods=['GET','POST'])
def auth():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        return redirect(url_for("auth"))
    #global user
    user=request.form['user']
    password=dbu.spass(user)
    if password[0]==request.form['pass']:
        friends = dbu.sfriend(user)
        for i in range(0,len(friends)):
            friends[i]=friends[i][0]
        #print(uuids)    
        hostname = socket.gethostname()    
        uuids = str(socket.gethostbyname(hostname))
        dbu.online(user,uuids)
        #session['username'] = user
        return redirect(url_for("home"))
    flash("wrong username or password")
    return redirect(url_for('login'))
#    return render_template("index.html", currTime = timerTime)

@app.route("/home")
def home():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        user=dbu.son(uuids)[0]
        friends = dbu.sfriend(user)
        for i in range(0,len(friends)):
            friends[i]=friends[i][0]
        return render_template("userprofile.html", currTime = timerTime, username = user, friendlist = friends, loggedin = True)
    return redirect(url_for("root"))

@app.route("/logout")
def logout():
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        user=dbu.son(uuids)[0]
        dbu.offline(user)
    return redirect(url_for("root"))

@app.route("/game", methods=["GET", "POST"])
def game():
    isloggedin = False
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        user=dbu.son(uuids)[0]
        isloggedin = True
    roomID = request.args['roomID'] if 'roomID' in request.args else 'Default';
    currGameNames = set()
    if roomID in games:
        for i in games[roomID]['players']:
            currGameNames.add(names[i])
        if user in currGameNames:
            flash('Already in this game!')
            return redirect(url_for('home'))
    return render_template("game.html", loggedin = isloggedin)

@socketio.on("joinRoom")
def joinRoom(roomID):
    if len(roomID) == 0:
        return
    if request.sid in rooms: #Checks if the user is already in a room
        if rooms[request.sid] == roomID:
            return
        leave_room(rooms[request.sid])
        if len(games[rooms[request.sid]]['players']) == 0: #Deletes game room if no-one is in it
            games.remove(rooms[request.sid])
    if roomID not in games: #Create new game
        games[roomID] = Game.newGame(request.sid)
        emit('yourturn', games[roomID]['offeredWords'])
    else:
        Game.addUser(games[roomID],request.sid)
    join_room(roomID) #Places user in a room
    rooms[request.sid] = roomID #Sets room of user in a dictionary for later use
    emit('joinRoom', roomID)
    emit('newPlayer', names[request.sid], broadcast = True, include_self = False, room = roomID)
    scoresToSend = {}
    for i in games[roomID]['points'].keys(): #Maps request.sids to the corresponding name before sending
        scoresToSend[names[i]] = games[roomID]['points'][i]
    emit('updateScores', scoresToSend)
    emit('highlightDrawer', names[games[roomID]['order'][games[roomID]['currDrawer']]])
    send('<b>' + names[request.sid] + ' has joined the room</b>', broadcast = True, room = roomID)

@socketio.on('connect')
def userConnect():
    newName = ''
    hostname = socket.gethostname()    
    uuids = str(socket.gethostbyname(hostname))
    if dbu.son(uuids):
        newName=dbu.son(uuids)[0]
    else:
        newName = 'Guest_' + ''.join(random.sample(string.ascii_lowercase, 8))
    names[request.sid] = newName
    print(newName)

@socketio.on('disconnect')
def disconn(): #Executed when a client disconnects from the server
    if request.sid in rooms:
        currGame = games[rooms[request.sid]]
        currDrawerRemoved = Game.removeUser(games[rooms[request.sid]], request.sid)
        if len(currGame['players']) == 0: #Deletes game room if no-one is in it
            games.pop(rooms[request.sid])
        elif currDrawerRemoved and len(currGame['order']) > currGame['currDrawer']:
            socketio.emit('yourturn', currGame['offeredWords'], room = currGame['order'][currGame['currDrawer']])
            emit('highlightDrawer', names[currGame['order'][currGame['currDrawer']]], broadcast = True, room = rooms[request.sid])
        socketio.send('<b>' + names[request.sid] + ' has left the room</b>')
        emit('playerLeave', names[request.sid], broadcast = True, room = rooms[request.sid])
        rooms.pop(request.sid)

@socketio.on('requestLines')
def returnLines(data):
    emit('recieveLines', games[rooms[request.sid]]['currLines'])

@socketio.on('clearBoard')
def clearBoard(data):
    currGame = games[rooms[request.sid]]
    if (request.sid != currGame['order'][currGame['currDrawer']] or currGame['currWord'] == ''):
        return
    currGame['currLines'] = []
    emit('clearBoard', None, broadcast = True, include_self = False, room = rooms[request.sid])

@socketio.on('newLine')
def newLine(line):
    currGame = games[rooms[request.sid]]
    # print(currGame['order'], currGame['currDrawer'])
    if (request.sid != currGame['order'][currGame['currDrawer']] or currGame['currWord'] == ''):
        return
    games[rooms[request.sid]]['currLines'].append(line);
    # print(line);
    emit('newLine', line, broadcast = True, include_self = False, room = rooms[request.sid])

@socketio.on('chooseWord')
def chooseWord(index):
    currGame = games[rooms[request.sid]]
    if (request.sid != currGame['order'][currGame['currDrawer']] or currGame['currWord'] != ''):
        return
    Game.chooseWord(currGame, index)
    currGame['timerTime'] = currGame['maxTime'] #Start drawing
    emit('startDrawing')
    send('<b>You have chosen ' + currGame['currWord'] + '</b>')
    currGame['currLines'] = []
    emit('clearBoard', None, broadcast = True, room = rooms[request.sid])
    emit('untint', broadcast = True, room = rooms[request.sid])

def countdown():
    global continueTimer, timerTime
    if continueTimer:
        threading.Timer(1, countdown).start()
        gamesCopy = list(games) #Used because gamesCopy will not be modified as the for loop is executed
        #Execute the following tasks every second
        for roomID in gamesCopy:
            try:
                currGame = games[roomID]
                # print(currGame['order'], currGame['currDrawer'], currGame['players'])
                currGame['timerTime'] -= 1
                if currGame['timerTime'] <= -1:
                    # print(currGame['gameState'])
                    if currGame['gameState'] == Game.DRAWING: #Executed when time runs out as a player is drawing
                        nextTurn(currGame, roomID)
                    elif currGame['gameState'] == Game.CHOOSING: #Executed when time runs out as a player is choosing a word
                        Game.chooseWord(currGame, None)
                        currGame['guessedCorrectly'] = set()
                        currGame['timerTime'] = currGame['maxTime'] #Start drawing
                        socketio.send('<b>You have chosen ' + currGame['currWord'] + '</b>', room = currGame['order'][currGame['currDrawer']])
                        socketio.emit('startDrawing', room = currGame['order'][currGame['currDrawer']])
                        currGame['currLines'] = []
                        socketio.emit('clearBoard', None, room = roomID)
                        socketio.emit('untint', room = roomID)
                # print(games[roomID]['timerTime'])
                socketio.emit('updateTimer', currGame['timerTime'], room = roomID)
            except:
                continue

def nextTurn(currGame, roomID):
    #guessedCorrectly.remove(request.sid)
    currGame['timerTime'] = 5 #Time a player has to choose a word
    socketio.emit('notyourturn', room = currGame['order'][currGame['currDrawer']])
    Game.nextUser(currGame)
    socketio.emit('yourturn', currGame['offeredWords'], room = currGame['order'][currGame['currDrawer']])
    socketio.emit('highlightDrawer', names[currGame['order'][currGame['currDrawer']]], room = roomID)
    socketio.send("<b>It is your turn to draw!</b>", room = currGame['order'][currGame['currDrawer']])
    scoresToSend = {}
    for i in currGame['points'].keys(): #Maps request.sids to the corresponding name before sending
        scoresToSend[names[i]] = currGame['points'][i]
    socketio.emit('updateScores', scoresToSend, room = roomID)
    socketio.emit('tint', room = roomID)
    currGame['guessedCorrectly'] = set()

@socketio.on('message')
def message(msg, methods=['GET','POST']):
    #print("Message " + msg)
    global currWord # TESTING
    if request.sid not in rooms:
        return
    currGame = games[rooms[request.sid]]
    currWord = currGame['currWord']
    #currWord = word.randword() # TESTING
    if len(msg) != 0:
        msg = msg[:200].replace('<','&lt;').replace('>','&gt;') #Caps message length at 200 characters and replaces HTML shenanigans
        if (request.sid != currGame['order'][currGame['currDrawer']]):
            guess = msg
            if request.sid in currGame['guessedCorrectly']:
                send("You can't guess again.")
                return
            if guess.lower() != currWord:
                send(msg, broadcast=True)
            else:
                Game.addPoints(currGame, request.sid) #Add points to guesser
                Game.addPoints(currGame, currGame['order'][currGame['currDrawer']], drawer = True) #Add points to drawer
                send("<b>Correct!!!</b>")
                if len(currGame['guessedCorrectly']) == 0:
                    currGame['timerTime'] = currGame['timerTime'] // 2 + 1
                currGame['guessedCorrectly'].add(request.sid)
                if len(currGame['guessedCorrectly']) >= len(currGame['players']) - 1: #Skip turn if everyone has guessed correctly
                    nextTurn(currGame, rooms[request.sid])
        else:
            send("<b>You can't chat while drawing.</b>")

        #print(guess == currWord)
        #if guess == currWord:
        #    send("Correct")


#@socketio.on("eventName")
#def fxn(data):
#   <Stuff to do upon recieving event>

if __name__ == '__main__':
    socketio.run(app, debug = True)
