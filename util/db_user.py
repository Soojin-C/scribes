import sqlite3 # ,os

# path = os.path.dirname(__file__)

DB_FILE="data/login.db"
# DB_FILE = path + DB_FILE
#makes users and friends table
def build():
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
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT username FROM users WHERE users.username=(?)"
    c.execute(command,(username))
    return c.fetchone()


#search/get password
def spass(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT password FROM users WHERE users.username=(?)"
    c.execute(command,(username))
    return c.fetchone()

#search/get friends
def sfriend(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="SELECT friend FROM friends WHERE friends.username=(?)"
    c.execute(command,(username))
    return c.fetchall()

#add user
def auser(username, password):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO users VALUES(?,?)"
    c.execute(command,(username, password))
    db.commit()
    db.close()

#add friend
def afriend(username):
    db=sqlite3.connect(DB_FILE)
    c=db.cursor()
    command="INSERT INTO friends VALUES(?)"
    c.execute(command,(username))
    db.commit()
    db.close()



if __name__ == '__main__':
    build()

