import sqlite3
conn = sqlite3.connect('SkateDB.db')
#conn.execute("PRAGMA foreign_keys = ON")
query = (''' CREATE TABLE IF NOT EXISTS Booking
		(id	INTEGER		PRIMARY KEY,
		start	DATETIME	NOT NULL,
		end	DATETIME	NOT NULL,
		text	TEXT		NOT NULL,
		color	TEXT		NOT NULL,
		bg		TEXT		NOT NULL,
		user_id	INTEGER		NOT NULL,
		FOREIGN KEY(user_id) REFERENCES Users(UID)
		);''')
conn.execute(query)
query = ('''CREATE INDEX idx_startBook ON Booking (start);''')
conn.execute(query)
query = ('''CREATE INDEX idx_endBook ON Booking (end);''')
conn.execute(query)
conn.close()