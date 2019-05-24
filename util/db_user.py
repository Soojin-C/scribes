import sqlite3

#makes users and friends table
def build():
    DB_FILE="data/login.db"
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"
    c.execute(command)
    command="CREATE TABLE IF NOT EXISTS friends(username TEXT, friend TEXT)"
    c.execute(command)
    db.commit()
    db.close()

#search/get user
def suser(username):
    DB_FILE="data/login.db"
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT username FROM users WHERE users.username=(?)"
    c.execute(command,(username))
    return c.fetchone()


#search/get password
def spass(username):
    DB_FILE="data/login.db"
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT password FROM users WHERE users.username=(?)"
    c.execute(command,(username))
    return c.fetchone()

#search/get friends
def sfriend(username):
    DB_FILE="data/login.db"
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT friend FROM friends WHERE users.username=(?)"
    c.execute(command,(username))
    return c.fetchall()

#add user
def auser(username, password):
    DB_FILE="data/login.db"
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO users VALUES(?,?)"
    c.execute(command,(username, password))
    db.commit()
    db.close()

#add friend
def afriend(username):
    DB_FILE="data/login.db"
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO friends VALUES(?)"
    c.execute(command,(username))
    db.commit()
    db.close()


