import os
import sys
from model.document_format import read_document_format

DOCUMENT_TABLE = 'document'

def upload_document(conn,document, name, content_type, file_extension, username, document_id = None):
    df = read_document_format(conn, mime_type=content_type)
    cur = conn.cursor()
    #df = document_format, dfi = document_format_id, dti = document_type_id
    if df:
        dfi = df[0][0]
        dti = df[0][4]
    if document_id:
        #sdf = stored_document_format
        sdf = cur.execute('SELECT document_format FROM document WHERE document_id = ?',(document_id,)).fetchall()[0][0]
        if dfi != sdf:
            return -1
        sql = 'UPDATE ' + DOCUMENT_TABLE + ' SET document =?, document_name = ?, updated_by = ? WHERE document_id = ? '
        cur.execute(sql,(document.read(), name,username,document_id))
        return document_id
    else:
        sql = 'INSERT INTO ' + DOCUMENT_TABLE + ' (document_name, document_type, document, created_by, document_format) VALUES (?,?,?,?,?)'
        cur.execute(sql,(name,dti,document.read(),username,dfi))
    
    conn.commit()
    conn.close()
    return cur.lastrowid
    