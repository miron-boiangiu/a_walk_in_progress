import sqlite3

connection = sqlite3.connect('database/database.db')

with open('database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()
