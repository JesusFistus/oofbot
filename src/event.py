import asyncio

eventlist = []
STOPKEY = '#'


async def user_input(channel, user):
    """Waits for a Message from a specifc user in a specific channel.

    Parameters
    -----------
    user: [:class:`discord.`]
        The DiscordClient object which contains all guild-specific information."""
    event = Event(channel, user)
    output = await event._input()
    if output is None:
        raise EventError(f': {str(event.channel)}')
    event._kill()
    return output


async def check_for_event(message):
    if eventlist:
        for event in eventlist:
            if event.channel == message.channel:
                if event.inputusers == [] or message.author in event.inputusers:
                    await event.queue.put(message)
                    return


class EventError(Exception):
    def __init__(self, message):
        self.message = message


class Event:
    def __init__(self, channel, user):
        self.user = user
        self.channel = channel

        self.queue = asyncio.Queue()

        self._check_current_events()
        eventlist.append(self)

    async def _input(self):
        message = await self.queue.get()

        if message.content == STOPKEY:
            self._kill()
            raise EventError(f'Event was aborted because the stopkey was received')

        return message

    def _kill(self):
        try:
            eventlist.remove(self)
        except ValueError:
            print('Could not remove event from eventlist')

    def _check_current_events(self):
        for event in eventlist:
            if event.channel == self.channel:
                raise EventError(f'There\'s already an ongoing event in this channel: {str(event.channel)}')
            elif event.user == self.user:
                raise EventError(f'There\'s already an ongoing event for this user: {str(event.user)}')
