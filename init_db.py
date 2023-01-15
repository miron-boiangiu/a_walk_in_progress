import sqlite3

connection = sqlite3.connect('config/database/database.db')

with open('config/database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()
