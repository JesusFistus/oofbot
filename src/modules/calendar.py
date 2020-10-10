import asyncio
import datetime
import dateutil.parser
import discord
import html2text as html2text
from pytz import timezone
from googleapihandler import get_entries


TIMEZONE = timezone('Europe/Berlin')


async def _wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now(TIMEZONE)
    await asyncio.sleep((dt - now).total_seconds())


class ReminderCalendar:
    """Represents a calendar that retrieves calendar entries from google kalender and sets corresponding reminders.

    Parameters
    -----------
    client: [:class:`client.DiscordClient`]
        The DiscordClient object which contains all guild-specific information.

    Attributes
    -----------

    reminders:  a list which contains all active reminders
    """

    def __init__(self, client):
        self.client = client
        self.reminders = []

        self.refresh()

    def refresh(self):
        """Fetches all google calendar entries and tries to set a reminder for each entry.
        If a fetched entry is already set as a reminder, the reminder will be overwritten."""

        # Fetches the next 5 entries per calendar
        entries = get_entries()

        # Set a reminder for every entry
        for entry in entries:
            self._set_reminder(entry)

    def _set_reminder(self, entry):
        """Sets a reminder for the """

        entry_id = entry['id']

        # If a reminder for this entry already exists, cancel it
        for reminder in self.reminders:
            if reminder.get_name() == entry_id:
                reminder.cancel()
                self.reminders.remove(reminder)

        # Create a new task for this entry
        new_reminder = asyncio.create_task(self._remind(entry), name=entry_id)
        self.reminders.append(new_reminder)

    async def _remind(self, entry):
        """The reminder courotine, that gets scheduled."""

        # Calculate the time when the reminder will be activated
        time = parse_time(entry, 'start')
        time -= datetime.timedelta(minutes=30)
        if time <= datetime.datetime.now(tz=TIMEZONE):
            return

        # Wait until reminder will be actived, except it got canceled
        try:
            await _wait_until(time)
        except asyncio.CancelledError:
            raise

        # Try to create embed form entry
        try:
            embed = create_reminder_embed(entry)
            await self.client.guild.text_channels[0].send(embed=embed)
            # TODO: Reminder muss im passenden announcment_channel gesendet werden
        except KeyError as e:
            print("could not create embed from entry dictionary:\n Ignoring entry.")
            print(e)


def create_reminder_embed(entry):
    """Creates a [:class:`discord.Embed`] object from an entry dict and returns it."""
    # Mandatory fields
    try:
        # TODO: flexible time
        message_content = f'{entry["organizer"]["displayName"]}: {entry["summary"]} in 30 Minuten!'
        desc_plain_text = html2text.html2text(entry['description'])
        start_time = parse_time(entry, 'start')

        message_embed = discord.Embed(description=desc_plain_text, colour=discord.Colour(0x2fb923),
                                      title=message_content)
    except KeyError as e:
        raise e

    # Optional field
    if 'location' in entry:
        location = entry['location']
        message_embed.add_field(name="Ort / URL", value=location, inline=False)

    message_embed.add_field(name="Datum", value=start_time.strftime("%a, %d.%m.%Y"), inline=False)
    message_embed.add_field(name="Startzeit", value=start_time.strftime("%H:%M"), inline=True)

    # Optional field
    if 'end' in entry:
        end_time = parse_time(entry, 'end')
        duration = end_time - start_time
        message_embed.add_field(name="Dauer", value=str(duration), inline=True)
        message_embed.add_field(name="Endzeit", value=end_time.strftime("%H:%M"), inline=True)

    return message_embed


def parse_time(entry, entry_time_key):
    """Gets the in :entry_time_key: specified time string from the entry dict
    and returns it as an datetime object"""

    if 'dateTime' in entry[entry_time_key]:
        time_unparsed = entry[entry_time_key]['dateTime']
        time = dateutil.parser.parse(time_unparsed)

    elif 'date' in entry[entry_time_key]:
        time_unparsed = entry[entry_time_key]['date']
        time = dateutil.parser.parse(time_unparsed).astimezone(TIMEZONE)

    else:
        print("No date or dateTime key in entry dict recieved from Google Calendar API. \n Ignoring entry.")
        raise KeyError

    return time
