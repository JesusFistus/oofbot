import pickle
from discord import __version__ as dcpy_version, Intents
from pathlib import Path
from sys import exit

from core import client


__version__ = '1.0'


# try to load the discord token from data/dctoken.pickle
tokenpath = Path(__file__).absolute().parent / 'data' / 'dctoken.pickle'

try:
    with tokenpath.open('rb') as file:
        token = pickle.load(file)
except FileNotFoundError:
    print('No discord-token found, use scripts/set_token.py to set one.\n'
          'Aborting start')
    exit()


print("-------------------------")
print(f"Discord.py version: {dcpy_version}")
print(f"EIT-BOT version: {__version__}")


intents = Intents.default()
intents.members = True

client = client.DiscordClient(intents=intents)
client.run(token)
