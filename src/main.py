import client
import config_handler as Config
import discord


__version__ = '0.0 testing'


print("--------------------")
print("Discord.py version")
print(discord.__version__)
print("--------------------")
print("EIT-BOT version")
print(__version__)


client = client.DiscordClient()
client.run(Config.get('TOKEN'))
