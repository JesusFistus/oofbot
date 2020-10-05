import discord

from database_handler import Student, Session
from event import user_input

roles = {}
study_groups = {"EIB3A", "EIB3B", "EMB3A", "EIB2W"}


# TODO: Nach vorhanden Rollen im Server schauen und speichern

async def check_roles(client):
    for guild in client.guilds:
        for role in guild.roles:
            if role.name.lower() == "student":
                roles['student'] = role


# TODO: Einführung ins Setup, Aktivierung auch möglich per DM

async def register_student(member):
    session = Session()
    if not session.query(Student).filter(Student.discord_id == member.id).all():
        await member.send("Regeln bestätigen:")  # TODO: Regeln hinzufügen
        await user_input(member.dm_channel, targetuser=member)
        await member.send("willst du gleich setup machen alla? dann mach !setup")
        student = Student(discord_id=member.id)
        await member.add_roles(roles['student'])
        session.add(student)
        session.commit()
        return


# TODO: Verfügbare Gruppen anzeigen lassen, vllt vorher nach Semester fragen und filtern

async def student_setup(message):
    session = Session()
    member = message.author
    student = session.query(Student).filter(Student.discord_id == member.id).first()
    if student:
        await member.send("```Willkommen im Studenten-Setup zur automatischen Rollenzuweisung"
                          " unseres EIT-Servers.\n"
                          "Damit wir auch innerhalb des Servers wissen wer du bist, "
                          "gib bitte deinen Vornamen ein```")

        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content
        await member.send("```Und jetzt bitte deinen Nachnamen.```")
        message = await user_input(member.dm_channel, targetuser=member)
        surname = message.content
        try:
            await member.edit(nick=f"{name} {surname}")
        except discord.Forbidden:
            await member.send("```Bist Admin du Kek!```")

        await member.send(f"```Hallo {name} {surname}, \n"
                          f"gib jetzt bitte noch deine Studiengruppe an,"
                          f"damit wir dich richtig zuordnen können. \n"
                          f"Dies sind die verfügbaren Studiengruppen {study_groups}```")

        message = await user_input(member.dm_channel, targetuser=member)
        study_group = message.content
        await member.add_roles(roles[f'{study_group}'])

        await member.send(f' ```Vielen Dank für die Einschreibung in unseren EIT-Server. \n'
                          f'Du wurdest der Studiengruppe {study_group} zugewiesen. \n'
                          f'Hiermit hast du das Setup abgeschlossen und du wirst \n'
                          f'direkt richtig in den Server eingetragen.\n'
                          f'Falls etwas mit deiner Eingabe nicht stimmt, \n'
                          f'führe bitte einfach nochmal das Setup aus und pass \n'
                          f'deine Eingabe an!```')


# TODO: Studenten nach einzelnen Parametern checken

async def check_students(client):
    session = Session()
    gatherlist = []
    for guild in client.guilds:
        for member in guild.members:
            query = session.query(Student).filter(Student.discord_id == member.id).first()
            if not query:
                return

# TODO: Zuweisungen in Discord an die gespeicherten Werte anpassen

# TODO: Setup zum Einschreiben in Kurse
# TODO: Anzeige aktiver Kurse
