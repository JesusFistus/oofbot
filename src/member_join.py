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
        if session.query(Student).filter(Student.discord_id == member.id).all():
            student = Student(discord_id=member.id)
            await member.send("Willkommen im Studenten-Setup zur automatischen Rollenzuweisung"
                              " unseres EIT-Servers. "
                              "Damit wir auch innerhalb des Servers wissen wer du bist "
                              "gib bitte deinen Vor-&Nachnamen ein."
                              "<Max Bauer>")
            message = await user_input(member.dm_channel, targetuser=member)
            student.name = message.content.split(' ')
            print(student)

    else:
        return
    # ToDo: Dialog zur Abfrage der Daten


def check_students():
    pass
