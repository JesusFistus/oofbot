import client
import discord
from confighandler import config

__version__ = '0.1'


print("--------------------")
print("Discord.py version")
print(discord.__version__)
print("--------------------")
print("EIT-BOT version")
print(__version__)

client = client.DiscordClient()
client.run(config.token)


# TODO: Kommentare für alles
# TODO: Für GitHub öffentlich vorbereiten
