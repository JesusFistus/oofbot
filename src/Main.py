import DCBot
import confighandler as Config
import discord

print("--------------------")
print("Discord.py version")
print(discord.__version__)
print("--------------------")
print("ReichstagBot version")
print(DCBot.__version__)


bot = DCBot.DiscordBot()
bot.run(Config.get('TOKEN'))
