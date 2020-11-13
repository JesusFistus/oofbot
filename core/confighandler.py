# TODO: full rewrite pls
import sys
import yaml
from discord.utils import get
from pathlib import Path


datapath = Path(__file__).absolute().parent.parent / 'data'
dialogspath = datapath / 'dialogs.yml'
guildpath = datapath / 'guild.yml'

# TODO: make prefix guild-specific
config = {'prefix': '!'}


with dialogspath.open('r') as file:
    dialogs = yaml.load(file, Loader=yaml.Loader)


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
        self.feeds = []

    def get_study_groups(self):
        """ Generator yielding all study_groups belonging to the guild"""

        for semester in self.semester:
            for study_group in semester.study_groups:
                yield study_group


def load_guild_config(client):
    with guildpath.open('r') as file:
        guild_dict = yaml.load(file, Loader=yaml.Loader)

    # discord.guild object
    guild_object = get(client.guilds, id=guild_dict['id'])

    # Guild not found
    if guild_object is None:
        print(f'Bot is not part of a guild with the id = {guild_dict["id"]}. \n aborting.')
        sys.exit()

    # get guild parameter as discord.objects
    client.guild = Guild(guild_object)
    client.guild.rules_channel = get(client.guild.discord_obj.text_channels, id=guild_dict['rules_channel'])
    client.guild.quicklinks = guild_dict['quicklink']
    client.guild.student_role = get(client.guild.discord_obj.roles, id=guild_dict['student_id'])

    # get semester parameter as dict
    client.guild.semester = []
    for semester in guild_dict['semester'].values():
        new_semester = Semester()
        new_semester.name = semester['name']
        announcement_channel = get(client.guild.discord_obj.text_channels, id=semester['announcement_channel'])  # TODO: Don't crash with missing or wrong entries in yml
        new_semester.announcement_channel = announcement_channel

        for group_id in semester['groups'].values():
            new_semester.study_groups.append(get(client.guild.discord_obj.roles, id=group_id))

        client.guild.semester.append(new_semester)

    print(f'Guild "{guild_object.name}" loaded successfully')
