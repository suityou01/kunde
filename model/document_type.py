DOCUMENT_TYPE_TABLE = 'document_type'

'''
CREATE TABLE "document_type" (
	"document_type_id"	INTEGER NOT NULL,
	"document_type"	TEXT NOT NULL,
	"active"	TEXT NOT NULL DEFAULT 'yes',
	"created"	INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"created_by"	TEXT NOT NULL DEFAULT 'sysadmin',
	"updated"	INTEGER,
	"updated_by"	TEXT,
	PRIMARY KEY("document_type_id" AUTOINCREMENT)
)
'''

def read_document_type(conn,document_type=None, document_type_id=None):
    cur = conn.cursor()
    sql = "SELECT document_type_id, document_type, created, created_by, updated, updated_by FROM " + DOCUMENT_TYPE_TABLE 
    if document_type:
        sql+= " WHERE document_type = ?"
        cur.execute(sql,(document_type,))
    elif document_type_id:
        sql+= " WHERE document_type_id = ?"
        cur.execute(sql,(document_type_id,))
    return cur.fetchall()