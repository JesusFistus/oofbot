import sys
import yaml
from discord.utils import get


class BotConfig(yaml.YAMLObject):
    """ Container for bot-specific settings read from config.yml

        Attributes
        -----------
        token:    The bots discord token
        prefix:   The command prefix
        presence: The bots discord presence
        """

    yaml_tag = u'BotConfig'

    def __init__(self, token, prefix, presence):
        self.token = token
        self.prefix = prefix
        self.presence = presence


with open('data/config.yml', 'r', encoding='utf8') as file:
    config = yaml.load(file, Loader=yaml.Loader)
    print('BotConfig loaded successfully')

with open('data/dialogs.yml', 'r', encoding='utf8') as file:
    dialogs = yaml.load(file, Loader=yaml.Loader)
    print('Dialogs loaded successfully')


# TODO: auslagern
class Semester:
    """ Represents a semester

        Attributes
        -----------
        name:                   Display name of the semester
        study_groups:           List of discord.role.Role objects representing the study_groups
        announcement_channel:   discord.TextChannel object used for announcements
        """

    def __init__(self):
        self.name = ''
        self.study_groups = []
        self.announcement_channel = None


class Guild:
    """ Represents a guild

        Attributes
        -----------
        discord_obj:    The corresponding discord.guild.Guild object
        semester:       List of Semester objects represented in the guild
        quicklinks:     String containing the quicklinks that gets added at the bottom of most embeds
        rules_channel:  discord.TextChannel object containing the rules
        student_role:   discord.Role object that gets assigned to a registered user
        """

    def __init__(self, discord_guild):
        self.discord_obj = discord_guild
        self.semester = []
        self.quicklinks = ''
        self.rules_channel = None
        self.student_role = None

    def get_study_groups(self):
        """ Generator yielding all study_groups belonging to the guild"""

        for semester in self.semester:
            for study_group in semester.study_groups:
                yield study_group


# TODO: rewrite
def load_guild_config(client):
    with open('data/guild.yml', 'r', encoding='utf8') as file:
        guild_dict = yaml.load(file, Loader=yaml.Loader)

    # discord.guild object
    guild_object = get(client.guilds, id=guild_dict['id'])

    # Guild not found
    if guild_object is None:
        print(f'Bot is not part of a guild with the id = {guild_dict["id"]}. \n aborting.')
        sys.exit()  # TODO: Programmstart abbrechen, Stacktrace sollte aber nicht geprinted werden

    # get guild parameter as discord.objects
    client.guild = Guild(guild_object)
    client.guild.rules_channel = get(client.guild.discord_obj.text_channels, id=guild_dict['rules_channel'])
    client.guild.quicklinks = guild_dict['quicklink']
    client.guild.student_role = get(client.guild.discord_obj.roles, id=guild_dict['student_id'])

    # get semester parameter as dict
    client.guild.semester = []
    for year, semester in guild_dict['semester'].items():
        new_semester = Semester()
        new_semester.name = semester['name']
        announcement_channel = get(client.guild.discord_obj.text_channels, id=semester['announcement_channel'])  # TODO: Don't crash with missing or wrong entries in yml
        new_semester.announcement_channel = announcement_channel

        for group_id in semester['groups'].values():
            new_semester.study_groups.append(get(client.guild.discord_obj.roles, id=group_id))

        client.guild.semester.append(new_semester)

    print(f'Guildconfig for guild "{guild_object.name}" loaded successfully')
