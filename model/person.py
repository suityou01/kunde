'''
CREATE TABLE "person" (
	"person_id"	INTEGER NOT NULL,
	"first"	TEXT NOT NULL,
	"last"	TEXT NOT NULL,
	"created"	INTEGER NOT NULL,
	"created_by"	TEXT NOT NULL,
	"updated"	INTEGER,
	"updated_by"	TEXT,
	"active"	TEXT NOT NULL DEFAULT 'yes',
	PRIMARY KEY("person_id" AUTOINCREMENT)
)
'''
PERSON_TABLE = 'person'
def create_person(conn, first, last, username):
    cur = conn.cursor()
    sql = 'INSERT INTO ' + PERSON_TABLE + ' (first, last, created_by) VALUES (?,?,?)'
    cur.execute(sql,(first,last,username))
    conn.commit()
    return cur.lastrowid  

def update_person(conn, id, first, last, username='sysadmin'):
    return

def delete_person(conn, id, username='sysadmin'):
    return

def read_person(conn, id):
    return