from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

rooms = {}

@app.route("/")
def root():
    return render_template("index.html")

#@socketio.on("eventName")
#def fxn(data):
#   <Stuff to do upon recieving event>

if __name__ == '__main__':
    socketio.run(app, debug = True)
