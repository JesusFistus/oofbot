import asyncio
import datetime
import dateutil.parser
from pytz import timezone
from googleapihandler import get_entries


class Calender:
    def __init__(self, client):
        self.client = client
        self.reminders = []

    def refresh(self):
        calendar_list = get_entries()
        # set a reminder for every event
        for calendar in calendar_list:
            for event in calendar['items']:
                self._set_reminder(event)

    async def _set_reminder(self, event):
        if 'dateTime' in event['start']:
            time_unparsed = event["start"]["dateTime"]
            time = dateutil.parser.parse(time_unparsed)
        elif 'date' in event['start']:
            time_unparsed = event['start']['date']
            time = dateutil.parser.parse(time_unparsed).astimezone(timezone('Europe/Berlin'))
            # TODO: Warum ist time hier manchmal +01:00 und manchmal +02:00 ?
            # print(time)
        else:
            print("No date or dateTime key in event dict recieved from Google Calendar API. \n Ignoring event.")
            return

        event_id = event['id']
        tasks = asyncio.all_tasks()

        # if a task for this event already exists, cancel it
        for task in tasks:
            if task.get_name() == event_id:
                task.cancel()

        # create a new task for this event
        new_reminder = asyncio.create_task(reminder(time, event), name=event_id)
        self.reminders.append(new_reminder)


async def calendar_refresh(client):
    calendar_list = get_entries()
    # set a reminder for every event
    reminder_list = []
    for calendar in calendar_list:
        for event in calendar['items']:
            reminder_list.append(set_reminder(client, event))
    await asyncio.gather(*reminder_list)


async def set_reminder(event):
    if 'dateTime' in event['start']:
        time_unparsed = event["start"]["dateTime"]
        time = dateutil.parser.parse(time_unparsed)
    elif 'date' in event['start']:
        time_unparsed = event['start']['date']
        time = dateutil.parser.parse(time_unparsed).astimezone(timezone('Europe/Berlin'))
        # TODO: Warum ist time hier manchmal +01:00 und manchmal +02:00 ?
        # print(time)
    else:
        print("No date or dateTime key in event dict recieved from Google Calendar API. \n Ignoring event.")
        return

    event_id = event['id']
    tasks = asyncio.all_tasks()

    # if a task for this event already exists, cancel it
    for task in tasks:
        if task.get_name() == event_id:
            task.cancel()

    # create a new task for this event
    new_reminder = asyncio.create_task(reminder(time, event), name=event_id)

    # now set it to be executed (unless it got cancelled)
    try:
        await new_reminder
    except asyncio.CancelledError:
        pass


async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now(timezone('Europe/Berlin'))
    await asyncio.sleep((dt - now).total_seconds())


async def reminder(time, event):
    await wait_until(time)
    await client.guild.text_channels[0].send(f'{event["summary"]} in 30 minuten!')
