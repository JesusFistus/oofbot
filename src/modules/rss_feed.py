import asyncio
import discord
import feedparser
import pickle


class RssFeed:
    def __init__(self, feed_link, channel):
        self.feed = None
        self.feed_link = feed_link
        self.channel = channel

    @staticmethod
    def get_entries(feed_obj):
        for feed_entry in feed_obj["entries"]:
            yield feed_entry

    async def refresh(self):
        new_feed = feedparser.parse(self.feed_link)

        if new_feed == self.feed:
            return

        elif self.feed is None:
            try:
                with open('feed_pickle', 'rb') as file:
                    self.feed = pickle.load(file)
                    file.close()

            except EOFError:
                await self.compare_feeds(new_feed)

        else:
            await self.compare_feeds(new_feed)

    async def compare_feeds(self, new_feed):
        for entry in self.get_entries(new_feed):
            if not self.feed:
                await self.send_feed_entry(entry)
            elif not [x for x in self.get_entries(self.feed)].count(entry):
                await self.send_feed_entry(entry)

        self.feed = new_feed

        with open('feed_pickle', 'wb') as file:
            pickle.dump(self.feed, file)
            file.close()

    async def send_feed_entry(self, entry):
        pass
        message = await self.channel.send(entry['link'])
        await self.edit_embed(message.id, entry)

    async def edit_embed(self, message_id, entry, timeout=5):
        counter = 0

        while 1:
            message = await self.channel.history().get(id=message_id)
            try:
                new_embed = message.embeds[0]
                description = entry['summary']

                if len(description) >= 2000:
                    description = description[:2000]

                new_embed.description = description
                await message.edit(content=None, embed=new_embed)
                return

            except IndexError or AttributeError:
                await asyncio.sleep(0.5)
                counter += 1

                if counter >= timeout * 2:
                    break
