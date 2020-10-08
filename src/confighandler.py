import yaml


class BotConfig(yaml.YAMLObject):
    yaml_tag = u'BotConfig'

    def __init__(self, token, prefix, presence):
        self.token = token
        self.prefix = prefix
        self.presence = presence


class RolesConfig(yaml.YAMLObject):
    yaml_tag = u'RolesConfig'

    def __init__(self, administrator, student, study_groups, guild):
        self.admin = administrator
        self.student = student
        self.study_groups = study_groups
        self.guild = guild


class Dialogs(yaml.YAMLObject):
    yaml_tag = u'Dialogs'

    def __init__(self, setup_dialogs):
        self.setup_dialogs = setup_dialogs


with open('data/config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.Loader)
    print('BotConfig loaded successfully')
    print(config.__dict__)

with open('data/roles.yml', 'r') as file:
    roles = yaml.load(file, Loader=yaml.Loader)
    print('GuildConfig loaded successfully')
    print(roles.__dict__)

with open('data/dialogs.yml', 'r') as file:
    dialogs = yaml.load(file, Loader=yaml.Loader)
    print('Dialogs loaded successfully')
    print(dialogs)
