import asyncio

eventlist = []


class Event:
    def __init__(self, targetchannel, targetusers=[]):
        self.inputusers = []
        self.queue = asyncio.Queue()
        self.channel = targetchannel
        if type(targetusers) is list:
            self.targetusers = targetusers
        else:
            self.targetusers = [targetusers]
        self.check_current_events()
        eventlist.append(self)

    async def input(self, targetusers=None):
        if targetusers is None:
            self.inputusers = self.targetusers
        elif type(targetusers) == list:
            self.inputusers = targetusers
        else:
            self.inputusers = [targetusers]
        message = await self.queue.get()
        if message.content == '#':
            self.kill()
            return
        return message

    def kill(self):
        eventlist.remove(self)

    def check_current_events(self):
        for event in eventlist:
            if event.channel == self.channel:  # TODO: Es sollte nur ein Event pro channel UND inputuser geben
                raise EventError(f'There\'s already an ongoing event in this channel: {str(event.channel)}')


async def user_input(targetchannel, targetuser=[]):
    event = Event(targetchannel, targetuser)
    output = await event.input()
    event.kill()
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
