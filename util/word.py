import random

words = open("static/wordlist.txt")
wordlist = words.readlines()

for word in wordlist:
    word.lower()
    word.strip()

print(wordlist)

def randword():
    word = random.choice(wordlist)
    print(word)
    return word
    