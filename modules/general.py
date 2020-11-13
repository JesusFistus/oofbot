import discord
from core import commands
from core.confighandler import config


class Help(commands.Command):
    usage = f'usage: {config["prefix"]}help <command>'
    arguments = 1

    @staticmethod
    async def exec(client, message):
        arguments = message.content.split(' ')

        if len(arguments) == 1:  # TODO: get text from dialogs.yml 
            embed = discord.Embed(title='Verfügbare Befehle:',
                                  colour=discord.Colour(0xff0000),
                                  description='_Für eine ausführe Beschreibung der Befehle tippe:_ \n '
                                              '\n'
                                              ' #help <Befehl>')

            for key, value in commands.commands.items():
                if value is not Help:
                    keystring = f'{key}:'
                    description = f'{value.description}'
                    embed.add_field(name=keystring, value=description, inline=False)

            quicklink(client, embed)
            await message.author.send(embed=embed)

        elif len(arguments) == 2:
            try:
                command_usage = commands.commands[arguments[1]].usage
                embed = discord.Embed(title=arguments[1],
                                      colour=discord.Colour(0xff0000),
                                      description=command_usage)
                quicklink(client, embed)
                await message.author.send(embed=embed)

            except KeyError:  # TODO: Send Embed instead of text and get text from dialogs.yml!
                await message.author.send(f'{arguments[1]} is not a valid command.'
                                          f'Type {config["prefix"]}help to get a list of all available commands.')


class Clear(commands.Command):
    description = "Clears messages in a channel."
    usage = f'{config["prefix"]}clear <amount> <users/roles>'
    arguments = 2
    permission = 2

    @staticmethod
    async def exec(client, message):
        pass


def quicklink(client: object, embed: object) -> object:
    embed.add_field(name="__Quicklinks:__", value=client.guild.quicklinks)
    return embed
