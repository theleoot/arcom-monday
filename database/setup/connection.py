import sqlite3

con = sqlite3.connect("./database/database/monday.db", check_same_thread=False)
cur = con.cursor()