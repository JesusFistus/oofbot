from database_handler import Student, Session, CalendarEntry
from event import user_input


# TODO: Setup zum Eintragen von Kalendereinträgen
# TODO: Benachrichtigung bevorstehender Einträge
# TODO: Zuweisung der Einträge zu Klassen und Personen
# TODO: Nach Einträgen filtern


async def calendar_setup(message):
    session = Session()
    member = message.author
    await member.send("```Willkommen im Kalender-Setup! \n"
                      "Um einen neuen Eintrag zu erstellen schreib <new> \n"
                      "und um einen vorhanden Eintrag zu verändern schreib <edit>````")

    message = await user_input(member.dm_channel, targetuser=member)
    if message.content == 'new':
        entry = CalendarEntry()
        await member.send("```Wie soll dein Kalendereintrag heißen?```")
        message = await user_input(member.dm_channel, targetuser=member)
        entry.name = message.content
        await member.send("```Zu welcher Kategorie gehört der Eintrag?```")
        message = await user_input(member.dm_channel, targetuser=member)
        entry.category = message.content
        await member.send("```Datum deines Eintrags?```")
        return

    elif message == "edit":
        pass
    else:
        await member.send("```Dies war kein gültiger Befehl!```")
        return
