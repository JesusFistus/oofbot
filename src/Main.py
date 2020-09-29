import client
import confighandler as Config
import discord

print("--------------------")
print("Discord.py version")
print(discord.__version__)
print("--------------------")
print("ReichstagBot version")
print(client.__version__)


client = client.DiscordClient()
client.run(Config.get('TOKEN'))
