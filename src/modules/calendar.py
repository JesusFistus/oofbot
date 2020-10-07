import asyncio
import datetime
import dateutil.parser
from pytz import timezone
from googleapihandler import get_entries


async def _wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now(timezone('Europe/Berlin'))
    await asyncio.sleep((dt - now).total_seconds())


class ReminderCalendar:
    def __init__(self, client):
        self.tz = timezone('Europe/Berlin')
        self.client = client
        self.reminders = []

        self.refresh()

    def refresh(self):
        calendar_list = get_entries()
        # set a reminder for every event
        for calendar in calendar_list:
            for event in calendar['items']:
                self._set_reminder(event)

    def _set_reminder(self, event):
        if 'dateTime' in event['start']:
            time_unparsed = event["start"]["dateTime"]
            time = dateutil.parser.parse(time_unparsed)
        elif 'date' in event['start']:
            time_unparsed = event['start']['date']
            time = dateutil.parser.parse(time_unparsed).astimezone(self.tz)
            # TODO: Warum ist time hier manchmal +01:00 und manchmal +02:00 ?
            # print(time)
        else:
            print("No date or dateTime key in event dict recieved from Google Calendar API. \n Ignoring event.")
            return

        time -= datetime.timedelta(minutes=30)
        if time <= datetime.datetime.now(tz=self.tz):
            return
        event_id = event['id']
        # if a reminder for this event already exists, cancel it
        for reminder in self.reminders:
            if reminder.get_name() == event_id:
                reminder.cancel()
                self.reminders.remove(reminder)

        # create a new task for this event
        new_reminder = asyncio.create_task(self._remind(time, event), name=event_id)
        self.reminders.append(new_reminder)

    async def execute_tasks(self):
        tasklist = []
        for reminder in self.reminders:
            tasklist.append(reminder)
        await asyncio.gather(*tasklist, return_exceptions=True)

    async def _remind(self, time, event):
        await _wait_until(time)
        await self.client.guild.text_channels[0].send(f'{event["summary"]} in 30 minuten!')
