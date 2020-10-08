import asyncio
import datetime
import dateutil.parser
import discord
import html2text as html2text
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
                event['calendar'] = calendar['summary']
                self._set_reminder(event)

    def _set_reminder(self, event):
        time = self.parse_time(event, 'start')
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

    def create_embed(self, event):
        try:
            message_content = f'{event["organizer"]["displayName"]}: {event["summary"]} in 30 Minuten!'  # TODO: flexible time
            desc_plain_text = html2text.html2text(event['description'])
            start_time = self.parse_time(event, 'start')
            end_time = self.parse_time(event, 'end')
            duration = end_time - start_time
            location = event['location']
        except KeyError:
            print("could not create embed from event dictionary")
            return

        message_embed = discord.Embed(description=desc_plain_text, colour=discord.Colour(0x2fb923),
                                      title=message_content)
        message_embed.add_field(name="Ort / URL", value=location, inline=False)
        message_embed.add_field(name="Datum", value=start_time.strftime("%a, %d.%m.%Y"), inline=False)
        message_embed.add_field(name="Startzeit", value=start_time.strftime("%H:%M"), inline=True)
        message_embed.add_field(name="Dauer", value=str(duration), inline=True)
        message_embed.add_field(name="Endzeit", value=end_time.strftime("%H:%M"), inline=True)

        return message_embed

    async def _remind(self, time, event):
        try:
            await _wait_until(time)
        except asyncio.CancelledError:
            raise
        await self.client.guild.text_channels[0].send("aisjodf")
        embed = self.create_embed(event)
        await self.client.guild.text_channels[0].send(embed=embed)

    def parse_time(self, event, event_time_key):
        if 'dateTime' in event[event_time_key]:
            time_unparsed = event[event_time_key]['dateTime']
            time = dateutil.parser.parse(time_unparsed)
        elif 'date' in event[event_time_key]:
            time_unparsed = event[event_time_key]['date']
            time = dateutil.parser.parse(time_unparsed).astimezone(self.tz)
            # TODO: Warum ist time hier manchmal +01:00 und manchmal +02:00 ?
            # print(time)
        else:
            print("No date or dateTime key in event dict recieved from Google Calendar API. \n Ignoring event.")
            return
        return time
