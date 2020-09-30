import sqlite3
import time


class Calendar:
    entries = []
    cursor = None
    db = None

    def load(self, dblocation):
        self.db = sqlite3.Connection(dblocation)
        self.cursor = self.db.cursor()
        self.entries.append(self._get_entries())

    def add(self, entry):
        self.entries.append(entry)
        self._save(entry)

    def _save(self, entry):
        self._insert_into_entries(entry.name, entry.allocation, entry.start,
                                  entry.all_day, entry.end, entry.description)

    def new(self, name, start, all_day=False, end=None, description=''):
        new_entry = CalenderEntry(name, start, all_day=all_day, end=end, description=description)
        self.entries.append(new_entry)
        self._save(new_entry)

    def today(self):
        outputstring = ''
        today = time.localtime()
        for entry in self.entries:
            start = time.gmtime(entry.start)
            if start.tm_year == today.tm_year and start.tm_mday == today.tm_mday and start.tm_mon == today.tm_mon:
                outputstring += str(entry) + '\n'
                print(entry)
        return outputstring

    def _insert_into_entries(self, *args):
        self.cursor.execute('''INSERT INTO Entries VALUES (?, ?, ?, ?, ?, ?)''', args)
        self.db.commit()

    def _get_entries(self):
        self.cursor.execute('''SELECT * FROM Entries''')
        entries = self.cursor.fetchall()
        output = []
        for entry in entries:
            new_entry = CalenderEntry(entry[0], entry[2], all_day=entry[3],
                                      description=entry[5], end=entry[4], allocation=entry[1])
            output.append(new_entry)
        return output


class CalenderEntry:
    def __init__(self, name, start, all_day=False, description='', end=0, allocation=''):
        self.name = name
        self.start = start
        self.all_day = all_day
        self.description = description
        self.end = end
        self.allocation = allocation

    def __repr__(self):
        return f'name:{self.name}\n' \
               f'allocation: {self.allocation}\n' \
               f'start: {self.start}\n'


c = Calendar()
c.load('C:/Users/Yannic Breiting/Documents/GitHub/oofbot/src/data/bot.db')
print(c.entries)
