import asyncio
import discord
from core.commands import command_handler
from core.confighandler import config, load_guild_config
from core.events import _check_for_event
from modules.student_calendar import Calendar
from modules.student_setup import Setup

# TODO: Discord Intents


class DiscordClient(discord.Client):

    def __init__(self, **options):
        super().__init__(loop=None, **options)
        self.calendar = None

    async def on_ready(self):
        print("-------------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("-------------------------")

        # load guild_config
        load_guild_config(self)

        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game("UwU"))

        # start calendar
        self.calendar = Calendar(self)
        await self.calendar.run()

    async def on_member_join(self, member):
        await Setup.exec(self, member=member)

    async def on_member_delete(self, member):
        pass

    async def on_message(self, message):
        # ignore own messages
        if message.author == self.user:
            return

        if message.content.startswith(config["prefix"]):
            await command_handler(self, message)
            return

        await _check_for_event(message)
