import commands
from confighandler import config


class Help(commands.Command):
    usage = f'```usage: {config.prefix}help <command>```'
    arguments = 1

    async def exec(client, message):
        arguments = message.content.split(' ')
        if len(arguments) == 1:
            outputstring = '```Verfügbare Befehle:\n'
            for key, value in commands.commands.items():
                if value is not Help:
                    outputstring += f'{config.prefix}{key}:  {value.description}\n'
            await message.author.send(outputstring)
        elif len(arguments) == 2:
            try:
                await message.author.send(commands.commands[arguments[1]].usage)
            except KeyError:
                await message.author.send(f'```{arguments[1]} is not a valid command.'
                                          f'Type {config.prefix}help to get a list of all available commands.```')


class Clear(commands.Command):
    description = "Clears messages in a channel."
    usage = f'{config.prefix}clear <amount> <users/roles>'
    arguments = 2
    permission = 2

    async def exec(dcbot, message):
        pass
