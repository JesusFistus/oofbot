import random as rnd
from io import BytesIO
import requests
from lib.utils import *
from os import listdir
import lib.confighandler as Config
from ttt import TicTacToe
from lib.event import Event
from lib.efficiency import Timer
import sympy
from sympy import plotting
import discord
from minesweeper import MineSweeper
import wolframalpha
from PIL import Image

prefix = Config.get('PREFIX')
wolframtoken = Config.get('WOLFRAMTOKEN')


# decides which command is called, calls all other functions in here
async def decide(dcbot, message):
    await message.author.create_dm()
    if message.content == prefix:
        command = 'help'
    else:
        command = message.content.split(' ')[0][1:].lower()

    if command == 'help':
        await h(dcbot, message)
    elif command == 'clear':
        await clear(dcbot, message)
    elif command == 'r':
        await r(dcbot, message)
    elif command == 'python':
        await python(dcbot, message)
    elif command == 'bash':
        await bash(dcbot, message)
    elif command == 'play':
        await play(dcbot, message)
    elif command == 'stt':
        await stt(dcbot, message)
    elif command == 'b':
        await b(dcbot, message)
    elif command == 'add':
        await add(dcbot, message)
    elif command == 'list':
        await list(dcbot, message)
    elif command == 'ttt':
        await ttt(dcbot, message)
    elif command == 'plot':
        await plot(dcbot, message)
    elif command == 'wa':
        await wolfram(dcbot, message)
    else:
        await message.author.dm_channel.send(
            f'**{command}** is not a valid command, type **{prefix}help**'
            f' for a list of available commands'
        )
        if type(message.channel) != discord.DMChannel:
            await message.delete()


# Help
async def h(dcbot, message):
    timer = Timer(message.content)
    await usage(dcbot, message, deletecommand=True)
    await message.author.dm_channel.send(
        f'An overview of all available commands:\n'
        f'**{prefix}clear** <amount=1> <members>  -  Deletes messages in a channel\n'
        f'**{prefix}r** <max=6>  -  Returns a random Integer between 0 and <max>\n'
        f'**{prefix}p** <options>  -  Controls for the python interpreter at #python\n'
        f'**{prefix}play** <file=random> -  Plays a random sound\n'
        f'**{prefix}list** - Show all available sounds\n'
        f'**{prefix}ttt** - Play a game of tictactoe\n'
        f'**{prefix}add** - Adds all Mp3s in this channel to the bot (only works in #bot-fileupload)\n'
        f'**{prefix}plot** <polynomial> - Plot any polynomial (only "x" and "y" are valid parameters)\n '
        f'**{prefix}wa** <query> - Ask Wolfram-Alpha anything\n'
    )
    timer.stop()
    return


# Clear
async def clear(dcbot, message):
    timer = Timer(message.content)
    botclear = False
    if not await usage(dcbot, message, admin=True, textchannel=True, deletecommand=True):
        return
    if message.content == f'{prefix}clear':
        deleteamount = 100
        botclear = True
    elif message.content == f'{prefix}clear all':
        await message.channel.send(f'Do you really want to delete ***every*** message in this channel?\n'
                                   f'type "clear all" to confirm')
        clearallevent = Event(dcbot, message.channel, targetusers=message.author)
        eventmessage = await clearallevent.input()
        clearallevent.kill()
        if eventmessage.content == 'clear all':
            deleteamount = 100000
        else:
            await message.channel.send(f'Invalid input!')
            return
    else:
        try:
            deleteamount = int(message.content.split(' ')[1])
            if deleteamount >= 1000:
                await message.channel.send(f'Do you really want to delete ***{deleteamount}*** '
                                           f'messages in this channel?\ntype "clear" to confirm')
                clearmuchevent = Event(dcbot, message.channel, targetusers=message.author)
                eventmessage = await clearmuchevent.input()
                clearmuchevent.kill()
                if not eventmessage.content == 'clear':
                    await message.channel.send(f'Invalid input!')
                    return
        except ValueError:
            await message.author.dm_channel.send(f'Invalid argument!')
            return

    # check if a message should be deleted or not
    def check(msg):
        if msg.pinned:
            return False
        elif botclear and msg.author == dcbot.user:
            return True
        elif not botclear and not message.mentions:
            return True
        elif not botclear and msg.author in message.mentions:
            return True

    await message.channel.purge(limit=deleteamount, check=check)
    timer.stop()


# Random
async def r(dcbot, message):
    timer = Timer(message.content)
    if message.content == f'{prefix}r':
        await message.channel.send(round(rnd.random() * 6))
        timer.stop()
        return
    try:
        argument = int(message.content.split(' ')[1])
    except ValueError:
        await message.author.dm_channel.send(f'Invalid argument, the argument has to be a single integer!')
        return
    await message.channel.send(round(rnd.random() * argument))
    timer.stop()


# Python
async def python(dcbot, message):
    timer = Timer(message.content)
    if not await usage(dcbot, message, admin=True, textchannel=True, deletecommand=True):
        return
    if message.content in [f'{prefix}python', f'{prefix}python start']:
        await dcbot.py.start(message)
    if message.content == f'{prefix}python stop':
        await dcbot.py.stop(message)
    timer.stop()


async def bash(dcbot, message):
    timer = Timer(message.content)
    if not await usage(dcbot, message, admin=True, textchannel=True, deletecommand=True):
        return
    if message.content in [f'{prefix}bash', f'{prefix}bash start']:
        await dcbot.bash.start(message)
    if message.content == f'{prefix}bash stop':
        await dcbot.bash.stop(message)
    timer.stop()


# Play
async def play(dcbot, message):  # TODO: Mehrere Lieder nacheinander abspielen
    timer = Timer(message.content)
    if not await usage(dcbot, message, textchannel=True, voicechannel=True, deletecommand=True):
        return
    if message.content == f'{prefix}play':
        await dcbot.voice.play_random_mp3(message.author.voice.channel)
    else:
        file = message.content.split(' ')[1].lower() + '.mp3'
        if file in listdir('data/MP3'):
            await dcbot.voice.play_mp3(message.author.voice.channel, file)
        else:
            await message.author.dm_channel.send(f'**{file}** doesn\'t exist!')
    timer.stop()


# Speech to text
async def stt(dcbot, message):
    timer = Timer(message.content)
    if not await usage(dcbot, message, admin=True, voicechannel=True, textchannel=True, deletecommand=True):
        return
    if message.content == f'{prefix}stt':
        await dcbot.stt.start(message)
        timer.stop()
    try:
        argument = message.content.split(' ')[1]
    except ValueError:
        await message.author.dm_channel.send(f'Invalid command, "{message.content}"')
        return
    if argument == 'start':
        await dcbot.stt.start(message)
    elif argument == 'stop':
        await dcbot.stt.stop()
    timer.stop()


# Bot Controls
async def b(dcbot, message):
    timer = Timer(message.content)
    if not await usage(dcbot, message, admin=True, deletecommand=True):
        return
    # Bot-Control help
    if message.content in [f'{prefix}b', f'{prefix}b help']:
        await message.author.dm_channel.send(
            f'List of available commands to control the bot:\n'
            f'{prefix}b presence <presence>\n'
        )
        timer.stop()
        return
    command = message.content.split(' ')[1]
    # Change Bots Presence
    if command == 'presence':
        argument = message.content[11:]
        await dcbot.change_presence(activity=discord.Game(argument))
    timer.stop()


# Add Files     TODO: in Modul 'Filehandler' auslagern, hier nur aufruf des Filehandlers
async def add(dcbot, message):
    timer = Timer(message.content)
    if not await usage(dcbot, message, admin=True, textchannel=True, deletecommand=True):
        return
    if message.channel.id != 720725292401819649:
        await message.channel.send(f'**{message.content}** can only be used in #bot-fileupload!')
        return
    filelist = []
    if message.content.lower() in [f'{prefix}add mp3', f'{prefix}add']:
        async for m in message.channel.history():
            for a in m.attachments:
                if a.filename.endswith('.mp3'):
                    if a.filename not in listdir('data/MP3'):
                        await a.save(f'data/MP3/{a.filename}')
                        filelist.append(a.filename)
                        timer.mark(a.filename)
                        await m.delete()
                    else:
                        await m.delete()
        if filelist:
            await message.channel.send(f'Successfully added: {filelist}')
        else:
            await message.channel.send(f'Couldn\'t add any new MP3s{filelist}')
    timer.stop()


# List mp3s (?list mp3)     TODO: über Filehandler realisieren
async def list(dcbot, message):
    timer = Timer(message.content)
    if message.content.lower() in [f'{prefix}list mp3', f'{prefix}list']:
        outputstring = ''
        for mp3 in sorted(listdir('data/MP3')):
            outputstring += mp3[:-4] + '\n'
        await message.channel.send(f'A list of all available sounds to use with **{prefix}play**:\n')
        if len(outputstring) >= 1980:
            for i in range(int(len(outputstring) / 1980) + 1):
                await message.channel.send(f'```\n{outputstring[(i * 1980):((i + 1) * 1980)]}```')
        else:
            await message.channel.send(f'```\n{outputstring}```')
    timer.stop()


# Tic Tac Toe
async def ttt(dcbot, message):
    if not await usage(dcbot, message, textchannel=True):
        return
    if message.content.lower() == f'{prefix}ttt':
        game = TicTacToe(dcbot, message)
        await game.start()


# Minesweeper
async def mines(dcbot, message):
    if not await usage(dcbot, message, textchannel=True):
        return
    if message.content.lower() == f'{prefix}mines':
        game = MineSweeper(dcbot, message)


# Plotter
async def plot(dcbot, message):
    x, y = sympy.symbols("x y")
    t = Timer(message.content)
    try:
        function = message.content.split(' ')[1]
    except IndexError:
        await message.author.dm_channel.send(f'Invalid Syntax!')

    if 'x' in function and 'y' not in function:
        try:
            graph = plotting.plot(function, show=False)
        except:
            await message.channel.send('Invalid input!')
        tempfileloc = 'data/temp_plot.png'
        graph.save(tempfileloc)
        await message.channel.send('', file=discord.File(tempfileloc))
    elif 'x' in function and 'y' in function:
        try:
            graph = plotting.plot3d(function, show=False)
            tempfileloc = 'data/temp_plot.png'
            graph.save(tempfileloc)
            await message.channel.send('', file=discord.File(tempfileloc))
        except:
            await message.channel.send('Invalid input!')


async def wolfram(dcbot, message):
    client = wolframalpha.Client(wolframtoken)
    try:
        query = message.content[4:]
    except IndexError:
        await message.author.dm_channel.send(f'Invalid Syntax!')
    try:
        async with message.channel.typing():
            res = client.query(query)
            for pod in res.pods:
                for sub in pod.subpods:
                    if sub['img']:
                        imgurl = sub['img']['@src']
                        imgtitle = pod['@title']
                        binimg = BytesIO(requests.get(imgurl).content)
                        await message.channel.send(imgtitle, file=discord.File(binimg, filename='wolframalpha.png'))
    except AttributeError:
        await message.channel.send(f'Wolfram Alpha doesn\'t understand your query: "{query}"\n'
                                   f'Try the following:\n'
                                   f'- Use different phrasing or notations\n'
                                   f'- Enter whole words instead of abbreviations\n'
                                   f'- Avoid mixing mathematical and other notations\n'
                                   f'- Check your spelling\n'
                                   f'- Give your input in English')
