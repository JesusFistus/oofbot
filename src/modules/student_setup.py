import discord
from discord.utils import get
import commands
from confighandler import config, roles, dialogs
from event import user_input


class Setup(commands.Command):
    description = 'Startet den Setup-Dialog. Hier kannst du dich registrieren, bzw. deine Angaben ändern.```'
    usage = f'```Tippe {config.prefix}setup um das Setup zu starten. Hiermit kannst du deine Registrierung abschließen,' \
            f'bzw. deine Angaben aktualisieren```'

    async def exec(client, message):
        member = get(await client.guild.fetch_members(limit=150).flatten(), id=message.author.id)
        if type(member) is not discord.Member:
            await message.author.send(f'```Hoppla!\n'
                                      f'Wie es scheint, bist du gar kein Mitglied des EIT-Discordservers```')
            return

        setup_embed = discord.Embed(description=dialogs['setup_dialog']['begin'], colour=discord.Colour(0x2fb923),
                                    title=dialogs['setup_dialog']['title'])

        await member.send(embed=setup_embed)

        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content
        try:
            await member.edit(nick=name)
        except discord.Forbidden:
            pass

        study_groups = roles.study_groups.keys()

        outputstring = ''
        for semester_key in study_groups:
            groups = dict.fromkeys(semester_key)
            print(groups)
            for group in groups:
                print(group)
                outputstring += group + '\n'

        setup_embed = discord.Embed(description=dialogs['setup_dialog']['group'].format(name, outputstring), colour=discord.Colour(0x2fb923),
                                    title=dialogs['setup_dialog']['title'])
        setup_embed.add_field(name="2. Semester", value='kot', inline=True)

        await member.send(embed=setup_embed)

        while True:
            message = await user_input(member.dm_channel, targetuser=member)
            study_group = message.content.upper()
            if study_group in groups:
                role = get(client.guild.roles, id=roles.study_groups[study_group])
                await member.add_roles(role)
                break
            else:

                setup_embed = discord.Embed(description=dialogs['setup_dialog']['end'], colour=discord.Colour(0x2fb923),
                                            title=dialogs['setup_dialog']['title'])
                await member.send(embed=setup_embed)

        setup_embed = discord.Embed(description=dialogs['setup_dialog']['error'], colour=discord.Colour(0x2fb923),
                                    title=dialogs['setup_dialog']['title'])

        await member.send(embed=setup_embed)

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
