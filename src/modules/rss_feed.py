import asyncio
import discord
import feedparser


class RssFeed:
    def __init__(self, feed_link, channel):
        self.feed = []
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

        # elif self.feed is None:
        #     self.feed = new_feed

        else:
            await self.compare_feeds(new_feed)

    async def compare_feeds(self, new_feed):
        for entry in self.get_entries(new_feed):
            if not self.feed:
                await self.send_feed_entry(entry)
            elif not [x for x in self.get_entries(self.feed)].count(entry):
                await self.send_feed_entry(entry)

        self.feed = new_feed

    async def send_feed_entry(self, entry):
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

# feed = RssFeed()
# feed.refresh_feed()
# print(feed)
