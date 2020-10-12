import discord
import yaml
from discord.utils import get
import commands
from confighandler import config, get_study_groups
from event import user_input


# TODO: Formatieren

class Setup(commands.Command):
    # TODO: Setup Docs
    """Represents Setup

        Parameters
        -----------

        Attributes
        -----------

        """
    description = 'Startet den Setup-Dialog. \n' \
                  ' Hier kannst du dich registrieren, bzw. deine Angaben ändern.'
    usage = f'Tippe {config.prefix}setup um das Setup zu starten. Hiermit kannst du deine Registrierung abschließen,' \
            f'bzw. deine Angaben aktualisieren#'

    @staticmethod
    async def exec(client, message):
        member = await client.guild.discord_obj.fetch_member(message.author.id)

        if type(member) != discord.member.Member:
            print('User is not part of the guild, ignoring')
            return

        # load dialogs
        with open('data/dialogs.yml', 'r', encoding='utf8') as file:
            dialogs = yaml.load(file, Loader=yaml.Loader)

        # send beginning message
        embed = discord.Embed(description=dialogs['setup_dialog']['begin'],
                              colour=discord.Colour(0x2fb923),
                              title=dialogs['setup_dialog']['title'])

        await member.send(embed=embed)

        # await name-input
        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content
        # TODO: Max 32. Char, testen alter
        try:
            await member.edit(nick=name)
        except discord.Forbidden:
            pass

        # send group_selection message
        embed = discord.Embed(description=dialogs['setup_dialog']['group_selection'].format(name=name),
                              colour=discord.Colour(0x2fb923),
                              title=dialogs['setup_dialog']['title'])

        for semester in client.guild.semester:
            group_string = ''
            for group in semester.study_groups:
                group_string += group.name + '\n'

            embed.add_field(name=semester.name, value=group_string, inline=True)

        await member.send(embed=embed)

        # loop until group_selection ended
        flag = True
        while flag:
            message = await user_input(member.dm_channel, targetuser=member)
            for study_group in get_study_groups(client.guild):
                if message.content.upper() == study_group.name:
                    await member.add_roles(study_group)
                    embed = discord.Embed(description=dialogs['setup_dialog']['end'].format(study_group=study_group),
                                          colour=discord.Colour(0x2fb923),
                                          title=dialogs['setup_dialog']['title'])

                    await member.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(description=dialogs['setup_dialog']['error'].format(message=message.content),
                                          colour=discord.Colour(0x2fb923),
                                          title=dialogs['setup_dialog']['title'])
            await member.send(embed=embed)


'''async def register_student(client, member):
    with open('data/dialogs.yml', 'r', encoding='utf8') as file:
        dialogs = yaml.load(file, Loader=yaml.Loader)

    name = member.name

    embed = discord.Embed(description=dialogs['register_dialog']['welcome'].format(name=name, rules=),
                          colour=discord.Colour(0x2fb923),
                          title=dialogs['register_dialog']['title'])
    #embed.add_field(name='Einführung', value=dialogs['register_dialog']['guide'])

    await member.send(embed=embed)'''

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
# TODO: Lösches des Embeds nach Vorlesungsende
