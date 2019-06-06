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
    command="CREATE TABLE IF NOT EXISTS online(user TEXT, uuid TEXT)"
    c.execute(command)
    db.commit()
    db.close()

#search/get user
def suser(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT username FROM users WHERE users.username=(?)"
    c.execute(command,username)
    output = c.fetchone()
    db.close()
    return output


#search/get password
def spass(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT password FROM users WHERE users.username=(?)"
    c.execute(command,username)
    output = c.fetchone()
    db.close()
    return output

#search/get friends
def sfriend(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT friend FROM friends WHERE friends.username=(?)"
    c.execute(command,username)
    output = c.fetchall()
    db.close()
    return output

#search/get friends
def son(uuid):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT user FROM online WHERE online.uuid=(?)"
    c.execute(command,(uuid,))
    output = c.fetchone()
    db.close()
    return output

#add user
def auser(username, password):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO users VALUES(?,?)"
    c.execute(command,(username, password))
    db.commit()
    db.close()

def online(username, uuid):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO online VALUES(?,?)"
    c.execute(command,(username, uuid,))
    db.commit()
    db.close()

def offline(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="DELETE FROM online WHERE user=(?)"
    c.execute(command,username)
    db.commit()
    db.close()
    
    
#add friend
def afriend(username,friend):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO friends VALUES(?,?)"
    c.execute(command,(username,friend))
    db.commit()
    db.close()



if __name__ == '__main__':
    build()
