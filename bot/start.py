import pickle
from discord import __version__ as dcpy_version
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
    print('dctoken.pickle not found, use scripts/set.token.py to set a discord token.\n'
          'Aborting start')
    exit()


print("-------------------------")
print(f"Discord.py version: {dcpy_version}")
print(f"EIT-BOT version: {__version__}")

client = client.DiscordClient()
client.run(token)
