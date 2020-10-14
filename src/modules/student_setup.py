import discord
import commands
from confighandler import config, get_study_groups, dialogs
from event import user_input


# TODO: Formatieren

class Setup(commands.Command):
    # TODO: Setup Docs
    """Represents the Setup Command.

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
    async def exec(client, message=None, member=None):
        if message:
            member = await client.guild.discord_obj.fetch_member(message.author.id)

        # check if member is part of the guild
        if type(member) != discord.member.Member:
            print('User is not part of the guild, ignoring')
            return

        # send beginning message
        embed = discord.Embed(description=dialogs['setup_dialog']['begin'],
                              colour=discord.Colour(0x2fb923),
                              title=dialogs['setup_dialog']['title'])

        await member.send(embed=embed)

        # await name-input
        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content

        # TODO: Max 32. Char, testen alter

        # change name to user_message
        try:
            await member.edit(nick=name)

        except discord.Forbidden:
            pass

        # send group_selection message
        embed = discord.Embed(description=dialogs['setup_dialog']['group_selection'].format(name=name),
                              colour=discord.Colour(0x2fb923),
                              title=dialogs['setup_dialog']['title'])

        # list of all available study_group
        for semester in client.guild.semester:
            group_string = ''

            for group in semester.study_groups:
                group_string += group.name + '\n'

            # create field for every semester
            embed.add_field(name=semester.name, value=group_string, inline=True)

        await member.send(embed=embed)

        # loop until group_selection ended
        flag = True

        while flag:
            message = await user_input(member.dm_channel, targetuser=member)

            for study_group in get_study_groups(client.guild):

                # add role corresponding to message_content
                if message.content.upper() == study_group.name:
                    """for member_role in member.roles:
                        if member_role == study_group:

                            # remove study_groups from member
                            # TODO: HELP! Entfernt nicht die Rolle
                            try:
                                await member.remove_roles(member_role, atomic=True)
                                print('nice')
                            except:
                                print('madig')"""

                    # set member roles to student & input study_group
                    await member.add_roles(study_group)
                    await member.add_roles(client.guild.student_role_obj)

                    # embed after succesful setup_completion
                    embed = discord.Embed(description=dialogs['setup_dialog']['end'].format(study_group=study_group),
                                          colour=discord.Colour(0x2fb923),
                                          title=dialogs['setup_dialog']['title'])

                    await member.send(embed=embed)
                    return

            else:
                # error_message for invalid message
                embed = discord.Embed(description=dialogs['setup_dialog']['error'].format(message=message.content),
                                        colour=discord.Colour(0x2fb923),
                                        title=dialogs['setup_dialog']['title'])

            await member.send(embed=embed)

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
# TODO: Lösches des Embeds nach Vorlesungsende
