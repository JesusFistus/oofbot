import sqlite3


location = 'data/bot.db'


db = sqlite3.connect(location)
db.row_factory = sqlite3.Row
cursor = db.cursor()


def get_entry(table, where):
    cursor.execute(f'SELECT * from {table} WHERE ?')
    return dict(cursor.fetchone())


def get_table(table):
    cursor.execute(f'SELECT * FROM {table}')
    outputlist = []
    for row in cursor.fetchall():
        outputlist.append(dict(row))
    return outputlist


def add_entry(table, dict):
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
    cursor.execute('INSERT INTO ? WHERE ? VALUES ?', (table, keystring, valuestring))
    db.commit()


def del_entry(table, where):
    cursor.execute(f'DELETE from {table} WHERE {where}')
    db.commit()


add_entry('Kalender', {'ID': 2, 'Betreff': 'test2', 'Start': 44, 'Ende': 55, 'Wiederholung': 0})
print(get_table('Kalender'))