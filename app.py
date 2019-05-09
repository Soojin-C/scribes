from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request
import threading
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

continueTimer = True
timerTime = 60 #Timer to be displayed
rooms = {}
currLines = []

@app.before_first_request #Executed upon startup
def setup():
    countdown() #Start countdown timer

@app.route("/")
def root():
    return render_template("index.html", currTime = timerTime)

@socketio.on('requestLines')
def returnLines(data):
    emit('recieveLines', currLines)

@socketio.on('clearBoard')
def clearBoard(data):
    currLines = []
    # print(currLines)
    emit('clearBoard', None, broadcast = True, include_self = False)

@socketio.on('newLine')
def newLine(line):
    currLines.append(line);
    # print(line);
    emit('newLine', line, broadcast = True, include_self = False)

def countdown():
    global continueTimer, timerTime
    if continueTimer:
        threading.Timer(1, countdown).start()
        #Execute the following tasks every second
        timerTime -= 1
        if timerTime <= -1:
            timerTime = 60
        socketio.emit('updateTimer', timerTime)

#@socketio.on("eventName")
#def fxn(data):
#   <Stuff to do upon recieving event>

if __name__ == '__main__':
    socketio.run(app, debug = True)
