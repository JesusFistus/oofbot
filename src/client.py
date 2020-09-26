import discord
import os
import confighandler as Config

__version__ = '0.0 test'

# channels
rules_Ch = 759123487649431575

prefix = Config.get('PREFIX')
dblocation = Config.get('DATABASELOCATION')


class DiscordBot(discord.Client):
    def __init__(self, **options):
        super().__init__(loop=None, **options)

    async def on_ready(self):
        # Presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(Config.get('PRESENCE')))
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")

        # Do smth on every member in every guild the bot is part of
        for guild in self.guilds:
            for member in guild.members:
                pass

    async def on_member_join(self, member):
        pass

    async def on_member_delete(self, member):
        pass

    async def on_message(self, message):
        #print(message.channel.id)
        pass

    async def on_voice_state_update(self, member, before, after):
        pass