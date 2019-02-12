import asyncio
import discord
from tinydb import TinyDB, Query, where
import random
import os
import re

# takes in the dice string and returns a list with the dice rolls. If the string could not be parsed, returns null.
def RollDice(DiceString):
    DiceParse = re.search(r"[0-9]+[d]{1}[0-9]+", DiceString)
    if DiceParse == None:
        return None
    else:
        DiceRange = DiceParse.group().split("d")
        DiceResults = list()
        if DiceRange[0] == "0" or DiceRange[1] == "0":
            return DiceResults
        else:
            for x in range(int(DiceRange[0])):
                result = random.randint(1,int(DiceRange[1]))
                DiceResults.append(result)
        return DiceResults

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='!roll'))

@client.event
async def on_message(message):
    if message.content.startswith("!roll"):
        ReturnMessage = ""
        List = RollDice(message.content)
        if List == None:
            ReturnMessage = "The dice string was unrecognized"
        elif len(List) == 0:
            ReturnMessage = "You cant print 0 dice..."
        elif len(List) == 1:
            ReturnMessage = "Your dice roll is: {0}".format(List)
        else:
            ReturnMessage = "Your dice rolls are: {0}".format(List) + "\n"
            ReturnMessage += "Your sum is: {0}".format(sum(List))
        await client.send_message(message.channel, ReturnMessage)


client.run('NTQ0MzczMDMzMTU1MDM1MTQ2.D0KLeA.W7j2s8TGXpotlJbUZd98X_adJwM')
