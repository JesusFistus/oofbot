import discord

import commands
from confighandler import config


class Help(commands.Command):
    usage = f'usage: {config.prefix}help <command>'
    arguments = 1

    async def exec(client, message):
        arguments = message.content.split(' ')

        if len(arguments) == 1:
            embed = discord.Embed(title='Verfügbare Befehle:',
                                  colour=discord.Colour(0xff0000),
                                  description='_Für eine ausführe Beschreibund der Befehle tippe:_ \n '
                                              '\n'
                                              ' #help <Befehl>')

            for key, value in commands.commands.items():
                if value is not Help:
                    keystring = f'{key}:'
                    description = f'{value.description}'
                    embed.add_field(name=keystring, value=description, inline=False)

            embed.add_field(name="__Quicklinks:__", value=' [HM-Startseite](https://www.hm.edu/) '
                                                          ' [Moodle](https://moodle.hm.edu/my/) '
                                                          ' [Primus](https://www3.primuss.de/cgi-bin/login/index.pl?FH=fhm) ')
            await message.author.send(embed=embed)

        elif len(arguments) == 2:
            try:
                command_usage = commands.commands[arguments[1]].usage
                embed = discord.Embed(title=arguments[1],
                                      colour=discord.Colour(0xff0000),
                                      description=command_usage)
                embed.add_field(name="__Quicklinks:__", value='[HM-Startseite](https://www.hm.edu/)'
                                                              '[Moodle](https://moodle.hm.edu/my/)'
                                                              '[Primus](https://www3.primuss.de/cgi-bin/login/index.pl?FH=fhm)')
                await message.author.send(embed=embed)

            except KeyError:
                await message.author.send(f'{arguments[1]} is not a valid command.'
                                          f'Type {config.prefix}help to get a list of all available commands.')


class Clear(commands.Command):
    description = "Clears messages in a channel."
    usage = f'{config.prefix}clear <amount> <users/roles>'
    arguments = 2
    permission = 2

    async def exec(dcbot, message):
        pass
