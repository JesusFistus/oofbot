from confighandler import config
import discord


# TODO Embed
# TODO Mehr commands


# Command Baseclass. Commands must subclass this
class Command:
    # TODO: Command Doc
    """Represents the Command.

        Parameters
        -----------

        Attributes
        -----------

        """
    description = ''  # short description, shown in !help
    usage = ''  # usage/long description, shown in !help <command>
    arguments = 0  # max. number of arguments the commands expects
    permission = 0  # role needed to use the command. 0: everyone, 1: "registered" members, 2: administrators

    # When the command is used right, this method will be executed.
    @staticmethod
    async def exec(client, message):
        pass


async def command_check(client, message):
    split = message.content.split(' ')
    command = split[0][1:]
    if command not in commands.keys():
        embed = discord.Embed(title=f'__{command} ist kein verfügbarer Befehl!__',
                              colour=discord.Colour(0xff0000),
                              description=f'Type **{config.prefix}** help to get a list of all available commands.')
        await message.author.send(embed=embed)
        return

    try:
        arguments = split[1:]
    except IndexError:
        arguments = ()
    if len(arguments) > commands[command].arguments:
        await message.author.send(f'```Wrong usage of {config.prefix}{command}!\n'
                                  f'Type _{config.prefix}help {command}_ to see the usage of the command.```')
        return

    await commands[command].exec(client, message)


from modules import general, student_setup

commands = {
    'help': general.Help,
    '': general.Help,
    'setup': student_setup.Setup
}
