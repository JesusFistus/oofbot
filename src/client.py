import discord
import config_handler as config
from commands import check_command
from student_management import register_student, check_students, check_roles
from event import check_events


intents = discord.Intents()
intents.members = True
client = discord.Client(intents=intents)

prefix = config.get('PREFIX')
dblocation = config.get('DATABASELOCATION')
presence = config.get('PRESENCE')


class DiscordClient(discord.Client):
    def __init__(self, **options):
        super().__init__(loop=None, **options)

    async def on_ready(self):
        await check_roles(self)
        print("--------------------")
        print('Logged in as')
        print(f"{str(self.user)}, {self.user.id}")
        print("--------------------")
        # Set presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game(presence))

        await check_students(self)


# TODO: Nochmal anschauen weil nicht rein kot

    async def on_member_join(self, member):
        await register_student(self, member)

    async def on_member_delete(self, member):
        pass

    async def on_message(self, message):
        await check_events(message)
        await check_command(message)

    async def on_voice_state_update(self, member, before, after):
        pass
