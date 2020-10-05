from confighandler import config


# Command Baseclass. Commands must subclass this
class Command:
    description = ''    # short description, shown in !help
    usage = ''          # usage/long description, shown in !help <command>
    arguments = 0       # max. number of arguments the commands expects
    permission = 0      # role needed to use the command. 0: everyone, 1: "registered" members, 2: administrators

    # When the command is used right, this method will be executed.
    async def exec(client, message):
        pass


async def command_check(client, message):
    content = message.content
    if content.startswith(config.prefix):
        split = content.split(' ')
        command = split[0][1:]
        if command not in commands.keys():
            await message.author.send(f'{command} is not a valid command.'
                                      f'Type {config.prefix}help to get a list of all available commands.')
            return

        try:
            arguments = split[1:]
        except IndexError:
            arguments = ()
        if len(arguments) > commands[command].arguments:
            await message.author.send(f'Wrong usage of {config.prefix}{command}!\n'
                                      f'Type _{config.prefix}help {command}_ to see the usage of the command.')
            return
        await commands[command].exec(client, message)

from modules import general, calendar, dialogs
commands = {
    'help': general.Help,
    '': general.Help,
    'setup': dialogs.Setup
}
