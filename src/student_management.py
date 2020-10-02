import asyncio
from database_handler import Student, Session
from event import user_input
import discord

roles = {}
study_groups = {}

# TODO: Beliebiege Rollen vergleichen

async def check_roles(client):
    for guild in client.guilds:
        for role in guild.roles:
            if role.name.lower() == "student":
                roles['student'] = role


# TODO: Einführung ins Setup, Aktivierung auch möglich per DM

async def register_student(client, member):
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


async def student_setup(message):
    session = Session()
    member = message.author
    student = session.query(Student).filter(Student.discord_id == member.id).first()
    if student:
        await member.send("```Willkommen im Studenten-Setup zur automatischen Rollenzuweisung"
                          " unseres EIT-Servers.\n"
                          "Damit wir auch innerhalb des Servers wissen wer du bist, "
                          " gib bitte deinen Vor & Nachnamen ein.\n"
                          "Halte dich bitte an diese Form -> Max Mustermann```")
        message = await user_input(member.dm_channel, targetuser=member)
        try:
            name = message.content.split(' ')
            student.name = name[0]
            student.surname = name[1]
        except IndexError:
            await member.send("```Leider hat da etwas nicht funktioniert. \n"
                              "Das Setup wird nochmal neu gestartet, bitte \n"
                              "achte auf die vorgegebene Schreibweise.``` \n")
            session.close()
            return await student_setup(message)
        await member.send(f"```Hallo {student.name} {student.surname},"
                          f" gib jetzt bitte noch deine Studien- \n"
                          f"gruppe an, damit wir dich richtig zuordnen können.```")
        message = await user_input(member.dm_channel, targetuser=member)
        study_group = message.content
        student.study_group = study_group
        await member.send(f' ```Vielen Dank für die Einschreibung in unseren EIT-Server. \n'
                          f'Du wurdest der Studiengruppe {study_group} zugewiesen. \n'
                          f'Hiermit hast du das Setup abgeschlossen und du wirst \n'
                          f'direkt richtig in den Server eingetragen.\n'
                          f'Falls etwas mit deiner Eingabe nicht stimmt, \n'
                          f'führe bitte einfach nochmal das Setup aus und pass \n'
                          f'deine Eingabe an!```')
        session.commit()


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
