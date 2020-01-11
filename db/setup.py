import sqlite3

conn = sqlite3.connect('kunde.db')
c = conn.cursor()

c.execute('''CREATE TABLE 
             (date text, trans text, symbol text, qty real, price real)''')