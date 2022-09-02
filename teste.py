import sqlite3

con = sqlite3.connect("System.db")

cur = con.cursor()

try:
    cur.execute("CREATE TABLE movie(title, year, score)")
except:
    pass