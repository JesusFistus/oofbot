import asyncio
import datetime
import dateutil.parser
from pytz import timezone

from googleapihandler import get_entries


# TODO: Benachrichtigung bevorstehender Einträge
# TODO: Zuweisung der Einträge zu Klassen und Personen
# TODO: Nach Einträgen filtern

# Get calendar entries


async def calendar_remember():
    events_list = get_entries()
    # The following should also be run constantly (every xy seconds) to synchronize the calendar
    # A possibility would be to set the name of each task to the unique event id
    # and checking whether that task already exists to avoid multiple tasks for the same event
    # https://stackoverflow.com/questions/41794205/how-to-set-name-for-asyncio-task
    for events in events_list:
        for event in events['items']:
            new_task(event)



def new_task(event):
    print(event)
    if 'dateTime' in event['start']:
        time_unparsed = event["start"]["dateTime"]
    elif 'date' in event['start']:
        time_unparsed = event['start']['date']
    else:
        print("No date or dateTime key in event object recieved from Google Calendar API. \n Ignoring event.")
        return
    time = dateutil.parser.parse(time_unparsed)
    loop = asyncio.get_event_loop()
    event_id = event['id']
    tasks = asyncio.all_tasks(loop=loop)
    for task in tasks:
        if task.get_name() == event_id:
            task.cancel()
    loop.create_task(run_at(time, send_message(event)), name=event_id)


async def send_message(event):
    print(event["start"])


async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now(timezone('Europe/Berlin'))
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt, coro):
    try:
        await wait_until(dt)
        return await coro
    except asyncio.CancelledError:
        return
