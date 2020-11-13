import pickle
from pathlib import Path
import sys
from os import rename

# the bots /data directory
datapath = Path(__file__).parent.parent.absolute() / 'bot' / 'data'
tokenpath = datapath / 'dctoken.pickle'
old_tokenpath = datapath / 'dctoken_old.pickle'

new_token = input('new token: ')

# if a dctoken.pickle file already exists, rename it to dctoken_old.pickle
# if that file already exists aswell, exit the script without doing anything
try:
    rename(datapath / 'dctoken.pickle', datapath / 'dctoken_old.pickle')
    print('existing dctoken.pickle was renamed to dctoken_old.pickle')
except FileNotFoundError:
    pass
except FileExistsError:
    print('dctoken.pickle as well as dctoken_old.pickle already exist.\n'
          'Delete, move or rename one of these files and restart the script to set a new token.')
    sys.exit()

with tokenpath.open('wb') as file:
    pickle.dump(new_token, file)
    print('new token successfully set.')
