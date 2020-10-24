from asyncio import Queue


# Ongoing UserInputEvents
eventlist = []

# If a User sends a message with this content while in an ongoing Event, the Event gets abortet
STOPKEY = '#'


async def user_input(channel, user):
    """
    Parameters
    ----------
    channel:    discord.TextChanel object the event is listening on
    user:       discord.Member object the event listens to

    Returns:
        The "cought" Discord Message Object
    """
    event = UserInputEvent(channel, user)
    output = await event._input()
    if output is None:
        raise EventError(f': {str(event.channel)}')
    event._kill()
    return output


async def _check_for_event(message):
    if eventlist:
        for event in eventlist:
            if event.channel == message.channel:
                if event.user == message.author:
                    await event.queue.put(message)
                    return


class EventError(Exception):
    def __init__(self, message):
        self.message = message


class UserInputEvent:
    """ Represents an ongoing UserInputEvent."""

    def __init__(self, channel, user):
        """

        Args:
            channel: Discord Channel Object the event is listening on
            user: Discord Member Object the event listens to
        """

        self.user = user
        self.channel = channel
        self.queue = Queue()

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
                event._kill()
                # raise EventError(f'There\'s already an ongoing event in this channel: {str(event.channel)}')
            elif event.user == self.user:
                event._kill()
                # raise EventError(f'There\'s already an ongoing event for this user: {str(event.user)}')
