import random , os

path = "static/wordlist.txt"
path = os.path.dirname(__file__) + "/../" + path

defaultWords = set(x.lower() for x in open(path,'r').read().split())
# print(defaultWords)

DRAWING = 0
CHOOSING = 1

def newGame(firstPlayer, maxTime = 10, maxRounds = 3, wordPool = defaultWords): #Creates a new game
    output = {}
    output['players'] = set() #request.sid
    output['players'].add(firstPlayer)
    output['correctPlayers'] = set() #Set of players who have correctly guessed the word
    output['order'] = [firstPlayer] #Player order
    output['currDrawer'] = 0 #Index for order
    output['wordPool'] = wordPool #Word pool
    output['offeredWords'] = random.sample(wordPool,3)#['','',''] #Ask player to choose: apple, pear, banana
    output['currWord'] = '' #apple
    output['wordDisplay'] = '' #__p__
    output['points'] = {firstPlayer : 0} #Dictionary request.sid : score
    output['maxTime'] = maxTime
    output['timerTime'] = 10 #Current timer
    output['maxRounds'] = maxRounds
    output['round'] = 1
    output['currLines'] = []
    output['gameState'] = CHOOSING
    output['guessedCorrectly'] = set()
    return output

def addUser(game,user): #Adds user to a game
    game['players'].add(user)
    game['points'][user] = 0
    insertPos = int(random.random() * len(game['order']))
    if insertPos <= game['currDrawer']:
        game['currDrawer'] += 1
    game['order'].insert(insertPos, user)

def removeUser(game,user):
    currDrawerRemoved = False
    game['players'].remove(user)
    if game['order'][game['currDrawer']] == user:
        nextUser(game, keepIndex = True)
        game['timerTime'] = 5
        game['gameState'] = CHOOSING
        currDrawerRemoved = True
    elif game['currDrawer'] > game['order'].index(user):
        game['currDrawer'] -= 1
    game['order'].remove(user)
    if user in game['guessedCorrectly']:
        game['guessedCorrectly'].remove(user)
    del game['points'][user]
    return currDrawerRemoved

def chooseWord(game, index):
    if type(index) != type(1) or index < 0 or index > 2:
        game['currWord'] = random.choice(game['offeredWords'])
    else:
        game['currWord'] = game['offeredWords'][index]
    game['gameState'] = DRAWING

def nextUser(game, keepIndex = False):
    game['gameState'] = CHOOSING
    game['offeredWords'] = random.sample(game['wordPool'], 3)
    game['currWord'] = ''
    if not(keepIndex): #Not executed if the current drawer is removed
        game['currDrawer'] += 1
    if game['currDrawer'] >= len(game['players']): #Increments round or ends game if all players have gone
        game['round'] += 1
        game['currDrawer'] = 0
        if game['round'] > game['maxRounds']:
            return 'Game End'
    print(game['offeredWords'])

def addPoints(game, user, drawer = False):
    if drawer:
        game['points'][user] += game['timerTime'] * 75 // game['maxTime']
    else:
        game['points'][user] += game['timerTime'] * 100 // game['maxTime']
    return game['points'][user]

def fillWordPool(game):
    words = open("static/wordlist.txt",'r').read().split()
    game['wordPool'] = set(x.lower() for x in words)

def randword(game):
    word = random.sample(game['wordPool'],1)
    return word

def getcurrDrawer(game):
    return game['currDrawer']


if __name__ == '__main__':
    currgame = newGame("playerid0")
    #fillWordPool(currgame)
    print(currgame)
    print(randword(currgame))
    addUser(currgame, "user0")
    print(getcurrDrawer(currgame))
    nextUser(currgame)
    print(getcurrDrawer(currgame))
