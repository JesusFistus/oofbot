import asyncio
import datetime
import dateutil.parser
import discord
import html2text as html2text
from pytz import timezone

from googleapihandler import get_entries
from modules.general import quicklink

TIMEZONE = timezone('Europe/Berlin')


async def _wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now(TIMEZONE)
    await asyncio.sleep((dt - now).total_seconds())


def create_reminder_embed(entry):
    """Creates a [:class:`discord.Embed`] object from an entry dict and returns it."""
    # Mandatory fields
    try:
        # TODO: flexible time; entry['reminders']['overrides'].get(xyz)['minutes'] oder ['hours'] usw.
        message_content = f'{entry["organizer"]["displayName"]}: __{entry["summary"]}__ *in 30 Minuten!*'

        if 'description' in entry:
            desc_plain_text = html2text.html2text(entry['description'])

        else:
            desc_plain_text = None

        start_time = parse_time(entry, 'start')

        if 'calendarColorId' in entry:
            embed_color = discord.Colour(int(entry['calendarColorId'].lstrip('#'), 16))

        else:
            embed_color = discord.Colour(0x000000)

        message_embed = discord.Embed(description=desc_plain_text, colour=embed_color,
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
        message_embed.add_field(name="Dauer", value=(str(duration)[:-3]), inline=True)
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


async def remind(client, entry):
    """The reminder courotine, that gets scheduled."""

    # Calculate the time when the reminder will be activated
    time = parse_time(entry, 'start')
    time -= datetime.timedelta(minutes=30)

    if time <= datetime.datetime.now(tz=TIMEZONE):
        return

    # Wait until reminder will be actived, except it got canceled
    try:
        await _wait_until(time)
        # print(f'{entry["summary"]} successfully triggered')

    except asyncio.CancelledError:
        raise

    # Try to create embed from entry
    try:
        embed = create_reminder_embed(entry)
        quicklink(client, embed)

    except KeyError:
        print("could not create embed from entry dictionary:\n Ignoring reminder.")
        return

    # Try to get the corresponding announcment_channel and send the embed
    for semester in client.guild.semester:
        for study_group in semester.study_groups:
            if study_group.name.lower() in entry["organizer"]["displayName"].lower():
                await semester.announcment_channel.send(embed=embed)
                return
    print("could not find a corresponding announcment channel to post the reminder.\n Ignoring reminder")


class Calendar:
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

    async def refresh(self):
        """Fetches all google calendar entries and tries to set a reminder for each entry.
        If a fetched entry is already set as a reminder, the reminder will be overwritten."""

        # Fetches the next 5 entries per calendar
        loop = asyncio.get_running_loop()
        entries = await loop.run_in_executor(None, get_entries)

        # Set a reminder for every entry
        for entry in entries:
            self._set_reminder(entry)

    def _set_reminder(self, entry):
        """Sets a reminder for the entry"""

        entry_id = entry['id']

        # If a reminder for this entry already exists, cancel it
        for reminder in self.reminders:
            if reminder.get_name() == entry_id:
                reminder.cancel()
                self.reminders.remove(reminder)

        # Create a new task for this entry
        new_reminder = asyncio.create_task(remind(self.client, entry), name=entry_id)
        self.reminders.append(new_reminder)
