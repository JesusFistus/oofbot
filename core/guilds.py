import yaml
from sys import exit

from core.confighandler import datapath
from core.modules import get_module

# Load guilds-config
try:
    with (datapath / 'guilds.yml').open('r') as file:
        guilds_config = yaml.load(file, Loader=yaml.Loader)
except FileNotFoundError:
    print('No guild-config found.\nAborting start')
    exit()


class Guild:
    def __init__(self, dc_guild_object):
        self.dc_obj = dc_guild_object
        self.name = self.dc_obj.name

        self.prefix = '!'
        self.modules = []
        self.default_role = self.dc_obj.default_role

        self.load_config(guilds_config)

    def load_config(self, guilds_config):
        # checks if a config for this guild exists
        if self.dc_obj.id not in guilds_config:
            print(f'No config for guild "{self.dc_obj.name}" found.\n'
                  f'Using default settings for this guild')
            return
        guild_config = guilds_config[self.dc_obj.id]

        if 'prefix' in guild_config:
            prefix = guild_config["prefix"]
            if type(prefix) is str:
                self.prefix = prefix
            else:
                print(f'Got wrong type for prefix-setting in config for {self.name}. Setting prefix to "!".')

        if 'modules' in guild_config:
            modules = guild_config['modules']
            if type(modules) is list:
                for module_name in modules:
                    if type(module_name) is str:
                        try:
                            self.modules.append(get_module(module_name))
                        except FileNotFoundError:
                            print(f'Module "{module_name}" not found in modules directory. Ignoring module import.')
                    else:
                        print(f'Got wrong type for module-setting in config')