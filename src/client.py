import asyncio
from typing import Optional, Any

import discord
from discord.utils import get

from commands import command_check
from confighandler import config
# from modules.dialogs import register_student
from event import check_for_event
from modules.calendar import calendar_refresh


class DiscordClient(discord.Client):
    def __init__(self, **options):
        super().__init__(loop=None, **options)

    async def on_ready(self):
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")
        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(config.presence))
        self.guild = get(self.guilds, id=config.guild)

        while True:
            print('calendar_refresh')
            await calendar_refresh(self)
            await asyncio.sleep(600)

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
