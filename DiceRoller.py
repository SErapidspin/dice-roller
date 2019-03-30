import asyncio
import discord
import random
import os
import re

# Constant stream of output for logging. Taken from https://stackoverflow.com/questions/50957031/how-to-make-discord-py-bot-run-forever-if-client-run-returns
async def task():
    await client.wait_until_ready()
    while True:
        await asyncio.sleep(1)
        print('Running')

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

# Handling of an exit from the discord client. Taken from https://stackoverflow.com/questions/50957031/how-to-make-discord-py-bot-run-forever-if-client-run-returns
def handle_exit():
    print("Handling")
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass


client = discord.Client()

while True:
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

    # Loop to restart the bot on discord server issue. Below code taken from https://stackoverflow.com/questions/50957031/how-to-make-discord-py-bot-run-forever-if-client-run-returns
    client.loop.create_task(task())
    try:
        client.loop.run_until_complete(client.start('NTQ0MzczMDMzMTU1MDM1MTQ2.D0KLeA.W7j2s8TGXpotlJbUZd98X_adJwM'))
    except SystemExit: #Handles the SystemExit that discord will send from server side 
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        print("Program ended")
        break
    
    print("Bot restarting")
    client = discord.Client(loop = client.loop)
