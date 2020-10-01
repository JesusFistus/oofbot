import asyncio

from database_handler import Student, Session
from event import user_input
import discord


roles = {}
study_groups = {}


async def check_roles(client):
    for guild in client.guilds:
        for role in guild.roles:
            if role.name.lower() == "student":
                roles['student'] = role


async def register_student(client, member):
    session = Session()
    if not session.query(Student).filter(Student.discord_id == member.id).all():
        await member.send("Regeln bestätigen:")
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
        await member.send("Willkommen im Studenten-Setup zur automatischen Rollenzuweisung"
                          " unseres EIT-Servers.\n"
                          "Damit wir auch innerhalb des Servers wissen wer du bist "
                          "gib bitte deinen Vor-&Nachnamen ein.\n"
                          "<Max Mustermann")
        message = await user_input(member.dm_channel, targetuser=member)
        name = message.content.split(' ')
        student.name = name[0]
        student.surname = name[1]
        await member.send(f"Hallo {student.name} {student.surname}"
                          f" gib jetzt bitte noch deine Studiengruppe an,"
                          f" damit wir dich gleich richtig zuordnen können.")
        message = await user_input(member.dm_channel, targetuser=member)
        study_group = message.content
        student.study_group = study_group
        await member.send(f'Vielen Dank! Du wurdest der Studiengruppe {study_group}'
                          f' zugewiesen. Damit hast du das Setup erfolgreich abgeschlossen.')
        session.commit()


async def check_students(client):
    session = Session()
    gatherlist = []
    for guild in client.guilds:
        for member in guild.members:
            query = session.query(Student).filter(Student.discord_id == member.id).first()
            if not query:
                print(member.name)
                gatherlist.append(register_student(client, member))
        print(gatherlist)
        await asyncio.gather(gatherlist)
