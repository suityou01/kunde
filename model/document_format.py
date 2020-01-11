DOCUMENT_FORMAT_TABLE = 'document_format'

'''
CREATE TABLE "document_format" (
	"document_format_id"	INTEGER NOT NULL,
	"document_format"	TEXT NOT NULL,
	"mime_type"	TEXT NOT NULL,
	"extension"	TEXT NOT NULL,
	"document_type_id"	INTEGER NOT NULL,
	"created"	INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"created_by"	TEXT NOT NULL DEFAULT 'sysadmin',
	"updated"	INTEGER,
	"updated_by"	TEXT,
	PRIMARY KEY("document_format_id" AUTOINCREMENT)
)
'''

def read_document_format(conn,mime_type=None, document_format_id=None):
    cur = conn.cursor()
    sql = "SELECT document_format_id, document_format, mime_type, extension, document_type_id, created, created_by, updated, updated_by FROM " + DOCUMENT_FORMAT_TABLE 
    if mime_type:
        sql+= " WHERE mime_type = ?"
        cur.execute(sql,(mime_type,))
    elif document_format_id:
        sql+= " WHERE document_format_id = ?"
        cur.execute(sql,(document_format_id,))
    
    return cur.fetchall()