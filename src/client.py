import asyncio
import discord
from commands import command_check
from confighandler import config, load_guild_config
from event import _check_for_event
from modules.calendar import Calendar
from modules.student_setup import Setup


class DiscordClient(discord.Client):

    def __init__(self, **options):
        super().__init__(loop=None, **options)
        pass

    async def on_ready(self):
        # load guild_config
        load_guild_config(self)

        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")

        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(config.presence))

        for member in self.guild.discord_obj.members:
            print(member.name)
        # create Calendar object
        self.calendar = Calendar(self)

        # calendar refresher
        while True:
            await self.calendar.refresh()
            await asyncio.sleep(30)

    async def on_member_join(self, member):
        await Setup.exec(self, member=member)

    async def on_member_delete(self, member):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(config.prefix):
            await command_check(self, message)
            return

        await _check_for_event(message)

    async def on_voice_state_update(self, member, before, after):
        pass
