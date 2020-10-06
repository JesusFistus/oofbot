import asyncio
import datetime
import dateutil.parser
from pytz import timezone

from googleapihandler import get_entries


# TODO: Benachrichtigung bevorstehender Einträge
# TODO: Zuweisung der Einträge zu Klassen und Personen
# TODO: Nach Einträgen filtern

# Get calendar entries


async def calender_remember():
    events = get_entries()
    # The following should also be run constantly (every xy seconds) to synchronize the calendar
    # A possibility would be to set the name of each task to the unique event id
    # and checking whether that task already exists to avoid multiple tasks for the same event
    # https://stackoverflow.com/questions/41794205/how-to-set-name-for-asyncio-task
    for event in events:
        t = event["start"]["dateTime"]
        timetime = dateutil.parser.parse(t)
    await create_loop(timetime)


async def create_loop(timetime):
    loop = asyncio.get_event_loop()
    loop.create_task(run_at(timetime, hello()))


async def hello():
    print("hello!")
    await asyncio.sleep(300)
    await calender_remember()


async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now(timezone('Europe/Berlin'))
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt, coro):
    await wait_until(dt)
    return await coro
