from confighandler import config
import discord


# TODO Embed


# Command Baseclass. Commands must subclass this
class Command:
    """ Command Baseclass. Commands must subclass this.

        Attributes
        -----------
        description:    Short description of what the command does
        usage:          Description of the command
        arguments:      The maximum number of arguments the command expects
        permission:     The Permission a user needs to use the command
        """
    description = ''
    usage = ''
    arguments = 0
    permission = 0

    # When the command is used right, this method will be executed.
    @staticmethod
    async def exec(client, message):
        pass


# TODO: Permission handling
async def command_handler(client, message):
    """ Handles execution of commands

    Parameters
    ----------
    client:     The client object
    message:    The message that holds the command
    """

    split = message.content.split(' ')
    command = split[0][1:]

    # checks if the command valid
    if command not in commands.keys():  # TODO: get text from dialogs.yml
        embed = discord.Embed(title=f'__{command} ist kein verfügbarer Befehl!__',
                              colour=discord.Colour(0xff0000),
                              description=f'Type **{config.prefix}** help to get a list of all available commands.')
        await message.author.send(embed=embed)
        return

    # Parses arguments from the command
    try:
        arguments = split[1:]
    except IndexError:
        arguments = ()

    # checks if the maximum amount of arguments is exceeded
    if len(arguments) > commands[command].arguments:  # TODO: get text from dialogs.yml
        await message.author.send(f'```Wrong usage of {config.prefix}{command}!\n'
                                  f'Type _{config.prefix}help {command}_ to see the usage of the command.```')
        return

    # Executes the command
    await commands[command].exec(client, message)


from modules import general, student_setup

# command assignment
commands = {
    'help': general.Help,
    '': general.Help,
    'setup': student_setup.Setup
}
