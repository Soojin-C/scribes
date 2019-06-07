import sqlite3
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

DB_FILE = DIR + "data/login.db"

#path = os.path.dirname(__file__)

#DB_FILE="data/login.db"
#DB_FILE = path + "/../" + DB_FILE
#makes users and friends table
def build():
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"
    c.execute(command)
    command="CREATE TABLE IF NOT EXISTS friends(username TEXT, friend TEXT)"
    c.execute(command)
    command="CREATE TABLE IF NOT EXISTS game(user TEXT, game TEXT)"
    c.execute(command)
    command="CREATE TABLE IF NOT EXISTS profile(user TEXT, pic TEXT)"
    c.execute(command)
    db.commit()
    db.close()

#search/get profile pictures
def spic(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT pic FROM profile WHERE username=?"
    c.execute(command,(username,))
    output = c.fetchone()
    print(output)
    db.close()
    return output

#add profile pictures
def apic(username,picurl):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO profile VALUES(?,?)"
    c.execute(command,(username,picurl,))
    db.commit()
    db.close()

#search/get user
def suser(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT username FROM users WHERE username=?"
    c.execute(command,(username,))
    output = c.fetchone()
    print(output)
    db.close()
    return output


#search/get password
def spass(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT password FROM users WHERE users.username=(?)"
    c.execute(command,(username,))
    output = c.fetchone()
    db.close()
    return output

#search/get friends
def sfriend(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT friend FROM friends WHERE friends.username=(?)"
    c.execute(command,(username,))
    output = c.fetchall()
    db.close()
    return output

#search/get friends
def sf(username,friend):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT friend FROM friends WHERE friends.user=(?),friends.friend=(?)"
    c.execute(command,(username,friend,))
    output = c.fetchone()
    db.close()
    return output

def sg(friend):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT user FROM game WHERE game.user=(?)"
    c.execute(command,friend,)
    output = c.fetchone()
    db.close()
    return output

#add user
def auser(username, password):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO users VALUES(?,?)"
    c.execute(command,(username, password,))
    db.commit()
    db.close()

def agame(user, room):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO game VALUES(?,?)"
    c.execute(command,(user, room,))
    db.commit()
    db.close()

def rgame(user):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="DELETE FROM game WHERE user=(?)"
    c.execute(command,(username,))
    db.commit()
    db.close()


#add friend
def afriend(username,friend):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO friends VALUES(?,?)"
    c.execute(command,(username,friend,))
    db.commit()
    db.close()



if __name__ == '__main__':
    build()
