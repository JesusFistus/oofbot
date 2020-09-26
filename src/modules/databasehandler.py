import sqlite3

dblocation = 'C:/Users/Yanni/Documents/GitHub/oofbot/src/data/bot.db'


db  = sqlite3.connect(dblocation)
cursor = db.cursor()


def get_table(table_name):
    for row in 