import feedparser


class RssFeed:
    def __init__(self):
        self.new_feed = None
        self.feed = None
        self.entries = []

    @staticmethod
    def get_entries(feed_obj):
        for feed_entry in feed_obj["entries"]:
            yield feed_entry

    def refresh_feed(self):
        self.new_feed = feedparser.parse("https://www.hm.edu/2/rss_feeds/newsrss/news_allg_rss.de.xml")

        if self.new_feed == self.feed:
            return

        elif self.feed is None:
            self.update_feed()

        else:
            self.compare_feeds()

    def compare_feeds(self):
        for entry in self.get_entries(self.new_feed):
            if not self.entries.count(entry):
                self.send_feed_entry()
                
        self.update_feed()
        
    def update_feed(self):
        self.feed = self.new_feed

        entry_list = []
        for entry in self.get_entries(self.feed):
            entry_list.append(entry)

        self.entries = entry_list

    def send_feed_entry(self, amount=0):
        pass


feed = RssFeed()
feed.refresh_feed()
print(feed)
