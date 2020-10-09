import yaml
from discord.utils import get


# TODO Docs
# TODO Vllt auslagern

class BotConfig(yaml.YAMLObject):
    yaml_tag = u'BotConfig'

    def __init__(self, token, prefix, presence):
        self.token = token
        self.prefix = prefix
        self.presence = presence


with open('data/config.yml', 'r', encoding='utf8') as file:
    config = yaml.load(file, Loader=yaml.Loader)
    print('BotConfig loaded successfully')
    print(config.__dict__)


class Semester:
    def __init__(self):
        self.year = None
        self.name = ''
        self.groups = []
        self.announcment_channel = None


class Guild:
    def __init__(self, discord_guild):
        self.discord_obj = discord_guild
        self.semester = []


def load_guild_config(client):
    with open('data/guild.yml', 'r', encoding='utf8') as file:
        guild_dict = yaml.load(file, Loader=yaml.Loader)
    guild_object = get(client.guilds, id=guild_dict['id'])
    client.guild = Guild(guild_object)
    client.guild.semester = []
    for year, semester in guild_dict['semester'].items():
        new_semester = Semester()
        new_semester.year = year
        new_semester.name = semester['name']
        announcment_channel = get(client.guild.discord_obj.text_channels, id=semester['announcment_channel'])
        new_semester.announcment_channel = announcment_channel
        for group_id in semester['groups'].values():
            new_semester.groups.append(get(client.guild.discord_obj.roles, id=group_id))
        client.guild.semester.append(new_semester)


def get_study_groups(guild):
    for semester in guild.semester:
        for group in semester.groups:
            yield group
