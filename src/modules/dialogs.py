import discord
from discord.utils import get

import commands
from confighandler import config, roles
from event import user_input


# TODO: Einführung ins Setup, Aktivierung auch möglich per DM

async def register_student(member):
        await member.send("Regeln bestätigen:")  # TODO: Regeln hinzufügen
        await user_input(member.dm_channel, targetuser=member)
        await member.send("willst du gleich setup machen alla? dann mach !setup")
        await member.add_roles(roles['student'])


class Setup(commands.Command):
    description = 'Startet den Setup-Dialog. Hier kannst du dich registrieren, bzw. deine Angaben ändern.'
    usage = f'Tippe {config.prefix}setup um das Setup zu starten. Hiermit kannst du deine Registrierung abschließen,' \
            f'bzw. deine Angaben aktualisieren'

    async def exec(client, message):
        member = get(await client.guild.fetch_members(limit=150).flatten(), id=message.author.id)

        print(member)
        if type(member) is not discord.Member:
            await message.author.send(f'Hoppla!\n'
                                      f'Wie es scheint, bist du gar kein Mitglied des EIT-Discordservers')
            return

        await member.send("```Willkommen im Studenten-Setup zur automatischen Rollenzuweisung"
                          " unseres EIT-Servers.\n"
                          "Damit wir auch innerhalb des Servers wissen wer du bist, "
                          "gib bitte deinen Vornamen ein```")

        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content
        try:
            await member.edit(nick=name)
        except discord.Forbidden:
            await member.send("```Bist Admin du Kek!```")

        groups = roles.study_groups.keys()
        outputstring = ''
        for group in groups:
            outputstring += group + '\n'

        await member.send(f"```Hallo {name}, \n"
                          f"gib jetzt bitte noch deine Studiengruppe an,"
                          f"damit wir dich richtig zuordnen können.\n"
                          f"Folgende Studiengruppen stehen zur auswahl:\n"
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
                          f'Hiermit hast du das Setup abgeschlossen und du wirst \n'
                          f'direkt richtig in den Server eingetragen.\n'
                          f'Falls etwas mit deiner Eingabe nicht stimmt, \n'
                          f'führe bitte einfach nochmal das Setup aus und pass \n'
                          f'deine Eingabe an!```')

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
