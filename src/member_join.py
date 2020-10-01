from databasehandler import Student, Session
from event import user_input


async def register_student(member, roles):
    # check if student is already known
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


async def setup_student(message):
    if message.content == '!setup':
        session = Session()
        member = message.author
        print(member.id)
        if session.query(Student).filter(Student.discord_id == member.id).all():
            student = Student(discord_id=member.id)
            session.add(student)
            await member.send("Willkommen im Studenten-Setup zur automatischen Rollenzuweisung"
                              " unseres EIT-Servers. "
                              "Damit wir auch innerhalb des Servers wissen wer du bist "
                              "gib bitte deinen Vor-&Nachnamen ein."
                              "<Max Bauer>")
            message = await user_input(member.dm_channel, targetuser=member)
            name = message.content.split(' ')
            student(name=name[0], surname=name[1])
            await member.send(f"Hallo {student.name} {student.surname}"
                              f" gib jetzt bitte noch deine Studiengruppe an"
                              f" damit wir dich gleich richtig zuordnen können")
            message = await user_input(member.dm_channel, targetuser=member)
            study_group = message.content
            student(study_group=study_group)
            session.add(student)
            await member.send(f'Vielen Dank! Du wurdest der Studiengruppe {study_group}'
                              f' zugewiesen. Damit hast du das Setup erfolgreich abgeschlossen.')
            session.commit()
    else:
        return
    # ToDo: Dialog zur Abfrage der Daten


def check_students():
    pass
