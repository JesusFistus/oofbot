import client
from confighandler import config
import discord


__version__ = '1.0'


print("--------------------")
print("Discord.py version")
print(discord.__version__)
print("--------------------")
print("EIT-BOT version")
print(__version__)

client = client.DiscordClient()
client.run(config.token)
