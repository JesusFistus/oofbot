import sqlite3
import discord


class DataBase:
    def __init__(self, location):
        self.location = location
        self.db = sqlite3.connect(self.location)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def get_entry(self, table, where):
        self.cursor.execute(f'SELECT * from {table} WHERE {where}')
        return dict(self.cursor.fetchone())

    def get_table(self, table):
        self.cursor.execute(f'SELECT * FROM {table}')
        outputlist = []
        for row in self.cursor.fetchall():
            outputlist.append(dict(row))
        return outputlist

    def add_entry(self, table, dict):
        keystring = ''
        valuestring = ''
        for key, value in dict.items():
            keystring += str(key) + ','
            if type(value) == str:
                valuestring += '"' + value + '",'
            else:
                valuestring += str(value) + ','
        keystring = keystring[:-1]
        valuestring = valuestring[:-1]
        self.cursor.execute(f'INSERT INTO {table} ({keystring}) VALUES ({valuestring})')
        self.db.commit()

    def del_entry(self, table, where):
        self.cursor.execute(f'DELETE from {table} WHERE {where}')
        self.db.commit()

    def update_entry(self, table, what, where):
        insertstring = ''
        if type(what) == dict:
            for key, value in what.items():
                if type(value) == str:
                    insertstring += str(key) + "= '" + value + "',"
                else:
                    insertstring += str(key) + "= " + str(value)
            insertstring = insertstring[:-1]
        else:
            insertstring = what
        self.cursor.execute(f'UPDATE {table} SET {insertstring} WHERE {where}')
        self.db.commit()

db = DataBase('C:/Users/Yanni/Documents/GitHub/oofbot/src/data/bot.db')
for row in db.get_table('kalender'):
    print(row['ID'])