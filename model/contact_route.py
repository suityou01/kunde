from model import person 
'''CREATE TABLE "contact_route" (
	"contact_route_id"	INTEGER NOT NULL COLLATE UTF16CI,
	"name"	TEXT NOT NULL COLLATE UTF16CI,
	"value"	TEXT,
	"created"	INTEGER NOT NULL,
	"created_by"	NUMERIC NOT NULL,
	"updated"	INTEGER,
	"updated_by"	TEXT,
	"active"	TEXT,
	"contact_route_type"	INTEGER NOT NULL DEFAULT 1,
	"org_id"	INTEGER,
	"person_id"	INTEGER,
	PRIMARY KEY("contact_route_id" AUTOINCREMENT),
	FOREIGN KEY("org_id") REFERENCES "org"("org_id")
)'''
def create_contact_route(conn, name, value ,orgid=None,personid=None,contact_route_type=1,username='sysadmin'):
    return 

def update_contact_route(conn, id, name, value, username='sysadmin'):
    return

def delete_contact_route(conn, id, username='sysadmin'):
    return

def read_contact_route(conn, id):
    return
