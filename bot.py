import os
import discord
import re
from random import randint
from discord.ext import commands
from discord.ext.commands import bot
false = False
true = True
#579885543635157003
#for debugging purposes
#players = [633081096669626400,569217141413511199,587297444249993216,666747515198111756,559097520563814420,466088544151273483,478341117075783681]
#8 player max
alphabet = ['','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
players = []
_playing = false
_celebrationUrl = "https://tenor.com/view/winner-gif-22069448"
_disgraceUrl = "https://tenor.com/view/failure-fail-effort-loser-losers-gif-16219069"
TOKEN = "OTE2MjA4ODI3ODU3MjU2NTAw.Yamz9g.ArtHWWvK-T1e_puOpfRcH_LZXuQ"
bot = commands.Bot(command_prefix="!")


class game():
    def __init__(self,word):
        self.gameInProgress = False
        self.readyPlayer = "<" + "@" + "!" + str(000000000000000000) + ">"
        self.guessedChars = []
        self.requiredChars = []
        self.gameWord = word
        self.guessedWord = ""
        self.guesses = 8
        for char in self.gameWord:
            self.requiredChars.append(char)
            self.guessedWord = self.guessedWord + "-"
        print("\n")
        print("init complete.")
        print(self.gameWord.strip())
        print(self.guessedWord)
        print(self.readyPlayer)

@bot.event
async def on_ready():
    print("Connected to Discord as " + str(bot.user))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    bountyUserId = re.findall("([\d]+)",newGame.readyPlayer)
    print(bountyUserId)
    print(str(message.author) + " said " + "\"" + message.content + "\"")
    if message.channel.name == "game":
        if newGame.gameInProgress == True:
           if message.author.id == int(bountyUserId[0]):
               #print("*&^*&(%&*^$&%$&)*&^(*&%^#^%&&(%&^&^*($#@#$%^&*&^%$#$%^&*")
               await update(message.content.lower().strip(),message)
        else:
            return

    #else:
    await bot.process_commands(message)


@bot.command()
async def join(ctx):
    playerId = ctx.message.author.id
    playerMention = "<" + "@" + "!" + str(playerId) + ">"
    message = ""
    if playerMention in players:
        message = playerMention + " you are already in the game!"
    elif len(players) == 8:
        message = playerMention + " sorry, this game is full!"
    else:
        players.append(playerMention)
        message = playerMention + " joined the game!"
    print(message)
    await ctx.send(message)

@bot.command()
async def leave(ctx):
    playerId = ctx.message.author.id
    playerMention = "<" + "@" + "!" + str(playerId) + ">" 
    if playerMention in players:
        players.remove(playerMention)
        message = playerMention + " left the game!"
        print(message)
        await ctx.send(message)


    
@bot.command()
async def start(ctx):
    if "<" + "@" + "!" + str(ctx.message.author.id) + ">" not in players:
        return
    if newGame.gameInProgress == True:
        await ctx.send("Game in progress")
        return
    if len(players) == 0:
        await ctx.send("There are no players!")
        return
    await ctx.send(players)
    await ctx.send("Game starting!")
    print("Starting a game with " + str(len(players)) + " player(s)")
    newGame.readyPlayer = players[0]
    await ctx.guild.create_text_channel("game")
    await gameSay(ctx)
    await messageGameChannel(ctx,newGame.guessedWord)
    await messageGameChannel(ctx,newGame.readyPlayer + "it's your turn.")
    newGame.gameInProgress = True
    

@bot.command()
async def cleanup(ctx):
    for channel in ctx.guild.channels:
        if channel.name == "game":
            await channel.delete()

@bot.command()
async def shutdown(ctx):
    if str(ctx.message.author.id) == "621083507870924831":
        print("Shutdown command issued.")
        await bot.close()

async def messageGameChannel(ctx,message):
    for channel in ctx.guild.channels:
        if channel.name == "game":
            await channel.send(message)

async def messageGeneralChannel(ctx,message):
    for channel in ctx.guild.channels:
        if channel.name == "general":
            await channel.send(message)

async def gameSay(ctx):
    for channel in ctx.guild.channels:
        if channel.name == "game":
            await channel.send("@everyone")


def init(playWord):
        guessedLetters = ""
        for char in playWord:
            guessedLetters = guessedLetters + "_"
        return guessedLetters



async def update(guess,ctx):
    if len(guess.strip()) > 1:
        #print("Comparing " + guess.lower().strip() + " to " + newGame.gameWord.lower().strip())
        if guess.lower().strip() == newGame.gameWord.lower().strip():
            await endGame(ctx,True)
            #await bot.close()
        else:
            await endGame(ctx,False)
            #await bot.close()
    elif guess.lower() not in alphabet:
        await ctx.channel.send("Invalid guess. " + "Guesses: %s/8" % newGame.guesses)
    elif guess in newGame.guessedChars:
        await ctx.channel.send("Duplicate guess. " + "Guesses: %s/8" % newGame.guesses)

    else:
        newGame.guessedChars.append(guess)
        newGame.guessedWord = rebuild(newGame.gameWord,newGame.guessedChars)
        if guess in newGame.requiredChars:
            await ctx.channel.send(guess + " is correct. " + "Guesses: %s/8" % newGame.guesses)
            newGame.readyPlayer = next(players,newGame.readyPlayer)
            #await ctx.channel.send("========================")
        else:
            newGame.guesses -= 1
            await ctx.channel.send(guess + " is incorrect. " + "Guesses: %s/8" % newGame.guesses)
            #await ctx.channel.send("========================")
            newGame.readyPlayer = next(players,newGame.readyPlayer)
            
    if newGame.guesses < 1:
        await endGame(ctx,False)

    elif newGame.guessedWord.lower().strip() == newGame.gameWord:
        await endGame(ctx,True)
    else:
        await ctx.channel.send(newGame.guessedWord)
        await messageGameChannel(ctx,newGame.readyPlayer + "it's your turn.")



def next(array,value):
    returnIndex = 0
    for item in array:
        if item == value:
            if array.index(item) + 1 > len(array) - 1:
                returnIndex = 0
            else:
                returnIndex = array.index(item) + 1
    return array[returnIndex]
    

def rebuild(word,guessedLetters):
    #sb is shorthand for stringBuilder
    sb = ""
    for x in range(0,len(word) ):
        if word[x] in guessedLetters:
            sb = sb + word[x]
        else:
            sb = sb + "-"
    #sb = sb + "-"
    return sb

async def endGame(ctx,win):
    if win == True:
        print("Win")
        await messageGeneralChannel(ctx,"The word was \'%s\'" % newGame.gameWord)
        await cleanup(ctx)
        await messageGeneralChannel(ctx,_celebrationUrl)
        await bot.close()
    else:
        print("Loss")
        await messageGeneralChannel(ctx,"The word was \'%s\'" % newGame.gameWord)
        await cleanup(ctx)
        await messageGeneralChannel(ctx,_disgraceUrl)
        await bot.close()

#for debugging purposes
newPlayers = []
for player in players:
    newPlayers.append("<" + "@" + "!" + str(player) + ">")
    players = newPlayers
print(players)
#input()
#10 guesses
#re.findall("([\d]+)",ctx.message.content)
wordList = open("list2.txt",'r')
wordArray = []
for line in wordList:
    wordArray.append(line.strip())
wordList.close()

os.system("cls")
newGame = game(wordArray[randint(0,len(wordArray) - 1)])
#input()
bot.run(TOKEN)