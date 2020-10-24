import discord
import commands
from confighandler import config, dialogs
from event import user_input, EventError


class Setup(commands.Command):
    description = 'Startet den Setup-Dialog. \n' \
                  ' Hier kannst du dich registrieren, bzw. deine Angaben ändern.'
    usage = f'Tippe {config.prefix}setup um das Setup zu starten. Hiermit kannst du deine Registrierung abschließen,' \
            f'bzw. deine Angaben aktualisieren'

    @staticmethod
    async def exec(client, message=None, member=None):
        """
        Gets executed when the setup command is issued. See module commands.py for more information.

        Args:
            client:
            message:
            member:

        Returns:

        """
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

        # loop until User tiped in a valid name
        while True:
            # Wait for User input
            try:
                message = await user_input(member.dm_channel, member)
                name = message.content
            except EventError as e:
                print(e)
                return

            # Check if User tiped in a valid name
            if len(name) < 32:
                break
            else:
                # send message if User did not type in a valid study_group, the User will be asked to try again
                embed = discord.Embed(
                    description=dialogs['setup_dialog']['name_to_long'].format(message=message.content),
                    colour=discord.Colour(0x2fb923),
                    title=dialogs['setup_dialog']['title'])
                await member.send(embed=embed)

        # change Users Nickname to tiped in Name
        try:
            await member.edit(nick=name)
        except discord.Forbidden:
            print(f'Could not change Nickname of User "{member.name}".\n Ignoring')

        # create group_selection embed
        embed = discord.Embed(description=dialogs['setup_dialog']['group_selection'].format(name=name),
                              colour=discord.Colour(0x2fb923),
                              title=dialogs['setup_dialog']['title'])

        # add embed_fields acording to study_groups in guildconfig
        for semester in client.guild.semester:
            group_string = ''

            for group in semester.study_groups:
                group_string += group.name + '\n'

            # create field for every semester
            embed.add_field(name=semester.name, value=group_string, inline=True)

        await member.send(embed=embed)

        flag = True

        # loop until User tiped in a valid study_group
        while flag:
            # Wait for user input
            try:
                message = await user_input(member.dm_channel, member)
            except EventError as e:
                print(e)
                return

            # Check if User tiped in a valid study_group
            for study_group in client.guild.get_study_groups():
                if message.content.upper() == study_group.name:

                    # break loop if input is a valid study_group
                    chosen_study_group = study_group
                    flag = False
                    break
            else:
                # send message if User did not type in a valid study_group, the User will be asked to try again
                embed = discord.Embed(
                    description=dialogs['setup_dialog']['study_group_invalid'].format(message=message.content),
                    colour=discord.Colour(0x2fb923),
                    title=dialogs['setup_dialog']['title'])
                await member.send(embed=embed)

        # On successful study_group selection, give User the student role
        await member.add_roles(client.guild.student_role)

        # Check if User already has study_group roles, if so, remove them
        for role in member.roles:
            if role in client.guild.get_study_groups():
                await member.remove_roles(role)

        # set members study_group according to chosen study_group
        try:
            await member.add_roles(chosen_study_group)
        except NameError:
            print(f'Something went wrong in setup of User "{member.name}".\n Aborting setup')
            return

        # send embed after setup completed successfully
        embed = discord.Embed(description=dialogs['setup_dialog']['end'].format(study_group=study_group),
                              colour=discord.Colour(0x2fb923),
                              title=dialogs['setup_dialog']['title'])

        await member.send(embed=embed)

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
