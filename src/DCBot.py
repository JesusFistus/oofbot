import discord
import commands as cmd
from lib import confighandler as Config, audio
from lib.interpreter import PythonInterpreter, BashInterpreter
from lib.databank import MemberManager, FileManager
#from SpeechToText import SpeechToText
import os
import random as rnd

__version__ = '0.1 betha'

from lib.utils import get_sounds

prefix = Config.get('PREFIX')
dblocation = Config.get('DATABASELOCATION')


class DiscordBot(discord.Client):
    def __init__(self, **options):
        super().__init__(loop=None, **options)
        self.py = PythonInterpreter()
        self.bash = BashInterpreter()
        self.voice = audio.VoiceClient()
        self.mm = MemberManager(dblocation)
        self.fm = FileManager(dblocation)
        self.eventlist = []
        self.afk_channel = []
        discord.opus.load_opus(Config.get('OPUSLOCATION'))

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game(Config.get('PRESENCE')))
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")
        for guild in self.guilds:
            self.afk_channel.append(guild.afk_channel)
            for member in guild.members:
                self.mm.add_member(member)

    async def on_member_join(self, member):
        self.mm.add_member(member)

    async def on_member_delete(self, member):
        self.mm.del_member(member)

    async def on_message(self, message):
        # print(message.channel.id)
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        # Check if message is a command
        try:
            if message.content[0] == prefix:
                await cmd.decide(self, message)
        except IndexError:
            pass
        # Check if message is an event input
        if self.eventlist:
            for event in self.eventlist:
                if event.channel == message.channel:
                    if event.inputusers == [] or message.author in event.inputusers:
                        await event.queue.put(message)
                        await message.delete()
                        return

        for sound in get_sounds():
            if sound in message.content:
                if message.author.voice.channel:
                    await self.voice.play_mp3(message.author.voice.channel, sound + '.mp3')

        # Messages into the python channel will be sent to the python-interpreter
        if message.channel.id in [718382399951470693, 717775566714961960]:
            if self.py.isalive():
                with message.channel.typing():
                    await self.py.send(message)

        if message.channel.id in [728598820195270686]:
            if self.bash.isalive():
                with message.channel.typing():
                    await self.bash.send(message)

        # MP3-attachments into the bot-fileupload channel will be downloaded to the MP3 diretory
        elif message.channel.id == 720725292401819649:  # TODO: in extra-modul 'Filehandler' auslagern
            if message.attachments is not []:
                for a in message.attachments:
                    if a.filename.endswith('.mp3'):
                        if a.filename not in os.listdir('data/MP3'):
                            await a.save(f'data/MP3/{a.filename}')
                            await message.delete()
                            await message.channel.send(f'"{a.filename}" successfully added!')

                        else:
                            await message.channel.send(f'**{a.filename}** already exists, you may'
                                                       f' change the filename to add your file.')

    async def on_voice_state_update(self, member, before, after):
        if member == self.user:
            return
        if before.channel is None and after.channel:
            if after.channel in self.afk_channel:
                return
            # plays only the first 7 seconds of a random sound
            audiosource = audio.cut_to_audiosource(rnd.choice(os.listdir('data/MP3')), 7)
            await self.voice.play(after.channel, audiosource)


<>