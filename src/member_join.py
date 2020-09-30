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
        return


def check_students():
    pass
