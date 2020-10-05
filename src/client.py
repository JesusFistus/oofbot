import dateutil
import discord
from discord.utils import get
import asyncio, datetime

from pytz import timezone

from confighandler import config
from commands import command_check
from modules.dialogs import register_student
from event import check_for_event
from googleapihandler import get_entries


class DiscordClient(discord.Client):
    def __init__(self, **options):
        super().__init__(loop=None, **options)
        # Get calendar entries
        self.events = get_entries()
        loop = asyncio.get_event_loop()
        for event in self.events:
            t = event.get("start")
            time = t.get("dateTime")
            timetime = dateutil.parser.parse(time)
            loop.create_task(self.run_at(timetime,
                                    self.hello()))

    async def on_ready(self):
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")
        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(config.presence))
        self.guild = get(self.guilds, id=config.guild)

    async def on_member_join(self, member):
        await register_student(member)

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

    async def wait_until(self, dt):
        # sleep until the specified datetime
        now = datetime.datetime.now(timezone('Europe/Berlin'))
        await asyncio.sleep((dt - now).total_seconds())

    async def run_at(self, dt, coro):
        await self.wait_until(dt)
        return await coro

    async def hello(self):
        print("hello!")
