import asyncio
import discord
import timeit
from commands import command_check
from confighandler import config, load_guild_config
from event import check_for_event
from modules.calendar import ReminderCalendar


class DiscordClient(discord.Client):
    def __init__(self, **options):
        super().__init__(loop=None, **options)
        self.timer = timeit.timeit()

    async def on_ready(self):
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")

        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(config.presence))
        # load guild_config
        load_guild_config(self)

        # create Calendar object
        self.calendar = ReminderCalendar(self)

        # calendar refresher
        while True:
            self.calendar.refresh()
            await asyncio.sleep(60)

    async def on_member_join(self, member):
        pass

    async def on_member_delete(self, member):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith(config.prefix):
            await command_check(self, message)
            return
        await check_for_event(message)

    async def on_voice_state_update(self, member, before, after):
        pass
