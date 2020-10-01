import discord
import config_handler as config
from commands import check_command
from student_management import register_student, check_students, student_setup
from event import check_events

prefix = config.get('PREFIX')
dblocation = config.get('DATABASELOCATION')
presence = config.get('PRESENCE')


class DiscordClient(discord.Client):
    roles = {'student': None}

    def __init__(self, **options):
        super().__init__(loop=None, **options)

    async def on_ready(self):
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")
        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(presence))
        for guild in self.guilds:
            for role in guild.roles:
                if role.name.lower() == "student":
                    self.roles['student'] = role

    async def on_member_join(self, member):
        await register_student(member, self.roles)

    async def on_member_delete(self, member):
        pass

    async def on_message(self, message):
        await check_events(message)
        await check_command(message)

    async def on_voice_state_update(self, member, before, after):
        pass
