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

        setup_embed = discord.Embed(description=dialogs['setup_dialog']['setup_begin'], colour=discord.Colour(0x2fb923),
                                    title='Studenten-Setup')

        await member.send(embed=setup_embed)

        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content
        try:
            await member.edit(nick=name)
        except discord.Forbidden:
            pass

        groups = roles.study_groups.keys()
        outputstring = ''
        for group in groups:
            outputstring += group + '\n'

        await member.send(f"```Hallo {name}, \n"
                          f"gib jetzt bitte noch deine Studiengruppe an, \n"
                          f"damit wir dich richtig zuordnen können.\n"
                          f"Folgende Studiengruppen stehen zur Auswahl:\n"
                          f"{outputstring}```")
        while True:
            message = await user_input(member.dm_channel, targetuser=member)
            study_group = message.content.upper()
            if study_group in groups:
                role = get(client.guild.roles, id=roles.study_groups[study_group])
                await member.add_roles(role)
                break
            else:
                await member.send(f"```Hoppla!\n"
                                  f"Wie es scheint ist {message.content} keine gültige Studiengruppe.\n"
                                  f"Gehe sicher, dass du eine der aufgelisteten Studiengruppen eingetippt hast.\n"
                                  f"Ist deine Studiengruppe nicht dabei? Dann kontaktiere bitte ```")

        await member.send(f' ```Vielen Dank für die Einschreibung in unseren EIT-Server. \n'
                          f'Du wurdest der Studiengruppe {study_group} zugewiesen. \n'
                          f'Hiermit hast du das Setup abgeschlossen und deine Angaben \n'
                          f'werden in den Server eingetragen.\n'
                          f'Falls etwas mit deiner Eingabe nicht stimmt, \n'
                          f'führe bitte einfach nochmal das Setup aus und pass deine Eingabe an!```')

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
