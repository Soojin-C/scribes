from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash

import threading
import os

# from scribble.util import db_user as dbu
# from scribble.util import Game

from util import db_user as dbu
from util import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app, ping_interval = 1, ping_timeout = 5, allow_upgrades = False)

continueTimer = True
timerTime = 60 #Timer to be displayed
rooms = {} #request.sid : roomID
games = {} #roomID : game info dictionary


@app.before_first_request #Executed upon startup
def setup():
    try:
        dbu.build()
    except:
        pass
    countdown() #Start countdown timer

@app.route("/")
def root():
    if 'username' in session:
        return redirect(url_for("home"))
    return render_template("index.html", currTime = timerTime)

@app.route("/login")
def login():
    if 'username' in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/reg")
def reg():
    if 'username' in session:
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/register", methods=["POST","GET"])
def regis():
    if 'username' in session:
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
    if 'username' in session:
        return redirect(url_for("auth"))

    try:
        global user
        user=request.form['user']
        password=dbu.spass(user)
        if password[0]==request.form['pass']:
            friends = dbu.sfriend(user)
            for i in range(0,len(friends)):
                friends[i]=friends[i][0]
            session['username'] = user
            return redirect(url_for("home"))
    except:
        flash("wrong username or password")
        return redirect(url_for('login'))
    flash("wrong username or password")
    return redirect(url_for('login'))
#    return render_template("index.html", currTime = timerTime)

@app.route("/home")
def home():
    if 'username' in session:
        friends = dbu.sfriend(user)
        for i in range(0,len(friends)):
            friends[i]=friends[i][0]
        return render_template("userprofile.html", currTime = timerTime, username = user, friendlist = friends)
    return redirect(url_for("root"))

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("root"))

@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html")

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
    join_room(roomID) #Places user in a room
    if roomID not in games: #Create new game
        games[roomID] = Game.newGame(request.sid)
        emit('yourturn', games[roomID]['offeredWords'])
    else:
        Game.addUser(games[roomID],request.sid)
    rooms[request.sid] = roomID #Sets room of user in a dictionary for later use
    emit('joinRoom', roomID)

@socketio.on('disconnect')
def disconn(): #Executed when a client disconnects from the server
    print(request.sid + "Left")
    if request.sid in rooms:
        currGame = games[rooms[request.sid]]
        Game.removeUser(games[rooms[request.sid]], request.sid)
        if len(currGame['players']) == 0: #Deletes game room if no-one is in it
            games.pop(rooms[request.sid])
        else:
            currGame['timerTime'] = 5 #Time a player has to choose a word
            socketio.emit('yourturn', currGame['offeredWords'], room = currGame['order'][currGame['currDrawer']])
        rooms.pop(request.sid)

@socketio.on('requestLines')
def returnLines(data):
    emit('recieveLines', games[rooms[request.sid]]['currLines'])

@socketio.on('clearBoard')
def clearBoard(data):
    games[rooms[request.sid]]['currLines'] = []
    # print(currLines)
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

def countdown():
    global continueTimer, timerTime
    if continueTimer:
        threading.Timer(1, countdown).start()
        #Execute the following tasks every second
        gamesCopy = list(games)
        for roomID in gamesCopy:
            currGame = games[roomID]
            print(currGame['order'], currGame['currDrawer'], currGame['players'])
            currGame['timerTime'] -= 1
            if currGame['timerTime'] <= -1:
                print(currGame['gameState'])
                if currGame['gameState'] == Game.DRAWING: #Executed when time runs out as a player is drawing
                    currGame['timerTime'] = 5 #Time a player has to choose a word
                    socketio.emit('notyourturn', room = currGame['order'][currGame['currDrawer']])
                    Game.nextUser(currGame)
                    socketio.emit('yourturn', currGame['offeredWords'], room = currGame['order'][currGame['currDrawer']])
                elif currGame['gameState'] == Game.CHOOSING: #Executed when time runs out as a player is choosing a word
                    Game.chooseWord(currGame, None)
                    socketio.send("<b>It is your turn to draw!</b>", room = currGame['order'][currGame['currDrawer']])
                    currGame['timerTime'] = currGame['maxTime'] #Start drawing
                    socketio.send('<b>You have chosen ' + currGame['currWord'] + '</b>', room = currGame['order'][currGame['currDrawer']])
                    socketio.emit('startDrawing', room = currGame['order'][currGame['currDrawer']])

            # print(games[roomID]['timerTime'])
            socketio.emit('updateTimer', currGame['timerTime'], room = roomID)

@socketio.on('message')
def message(msg, methods=['GET','POST']):
    #print("Message " + msg)
    global currWord # TESTING
    currGame = games[rooms[request.sid]]
    currWord = currGame['currWord']
    #currWord = word.randword() # TESTING
    if len(msg) != 0:
        if (request.sid != currGame['order'][currGame['currDrawer']]):
            guess = msg
            if guess != currWord:
                send(msg, broadcast=True)
            else:
                send("<b>Correct!!!</b>")
        else:
            send("<b>You can't chat during your turn.</b>")

        #print(guess == currWord)
        #if guess == currWord:
        #    send("Correct")


#@socketio.on("eventName")
#def fxn(data):
#   <Stuff to do upon recieving event>

if __name__ == '__main__':
    socketio.run(app, debug = True)
