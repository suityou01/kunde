from model import person
from model import contact_route 
from model import address 
from model import document_type 
'''CREATE TABLE "org" (
	"org_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"created"	INTEGER NOT NULL,
	"created_by"	TEXT NOT NULL,
	"updated"	INTEGER,
	"updated_by"	INTEGER,
	"active"	TEXT NOT NULL DEFAULT 'yes',
	PRIMARY KEY("org_id" AUTOINCREMENT)
)
)'''
ORG_TABLE = 'org'
ORG_PERSON_TABLE = 'org_person'
CONTACT_ROUTE_TABLE = 'contact_route'
CONTACT_ROUTE_TYPE_POSTAL_ADDRESS = 2
DOCUMENT_TABLE = 'document'

def create_org(conn, name, username):
    cur = conn.cursor()
    sql = 'INSERT INTO ' + ORG_TABLE + ' (name, created_by) VALUES (?,?)'
    cur.execute(sql,(name,username))
    conn.commit()
    return cur.lastrowid 

def update_org(conn, id, name, username='sysadmin'):
    cur = conn.cursor()
    sql = 'UPDATE ' + ORG_TABLE + ' SET name = ?, updated = CURRENT_TIMESTAMP, updated_by=? WHERE org_id = ?'
    cur.execute(sql,(name,username,id))
    conn.commit()
    return id

def delete_org(conn, id, username='sysadmin'):
    try:
        cur = conn.cursor()
        sql = "UPDATE " + ORG_TABLE + " SET active = 'no', updated = CURRENT_TIMESTAMP, updated_by =? WHERE org_id = ?"
        cur.execute(sql,(username, id))
        conn.commit()
        return True
    except Exception as e:
        print(str(e))
        return False

def read_org_by_id(conn, id):
    cur = conn.cursor()
    sql = "SELECT name, created, created_by, updated, updated_by, active FROM " + ORG_TABLE + " WHERE org_id = ?"
    cur.execute(sql,(id,))
    return cur.fetchall()
 
def read_org(conn, zip = '%', name='%', include_inactive = False):
    cur = conn.cursor()
    if zip.strip() !='%':
        sql="SELECT O.org_id, O.name, O.created, O.created_by, O.updated, O.updated_by FROM address A" \
            " INNER JOIN contact_route C ON C.address_id = A.address_id AND C.org_id IS NOT NULL AND C.active = 'yes'" \
            " INNER JOIN org O ON O.org_id = C.org_id AND O.active = 'yes'" 
        if zip.rstrip()[-1]=="%":
            sql+=" WHERE A.zip LIKE ? " 
        else:
            sql+=" WHERE A.zip = ? "
        sql+=" AND A.active "
        sql+=" IN ('yes','no')" if include_inactive == True else " = 'yes'" 
        sql+=" GROUP BY O.org_id, O.name, O.created, O.created_by, O.updated, O.updated_by"
        ret = cur.execute(sql,(zip,))
        return ret.fetchall()
    elif name.strip()[1:]!='%':
        sql = "SELECT O.org_id, O.name, O.created, O.created_by, O.updated, O.updated_by, O.active FROM org O" 
        if name.rstrip()[-1]=="%":
            sql+=" WHERE O.name LIKE ? " 
        else:
            sql+=" WHERE O.name = ? "
        sql+=" AND O.active " + "IN ('yes','no')" if include_inactive == True else " = 'yes'"
        sql+=" GROUP BY O.org_id, O.name, O.created, O.created_by, O.updated, O.updated_by"
        ret = cur.execute(sql,(name,))
        return ret.fetchall()
    else:
        return False

'''
CREATE TABLE "org_person" (
	"org_person_id"	INTEGER NOT NULL,
	"org_id"	INTEGER NOT NULL,
	"person_id"	INTEGER NOT NULL,
	"org_person_rel_type"	INTEGER NOT NULL,
	"created"	INTEGER NOT NULL,
	"created_by"	TEXT NOT NULL,
	"updated_by"	TEXT,
	"active"	TEXT NOT NULL DEFAULT 'yes',
	PRIMARY KEY("org_person_id")
)
'''
def add_existing_person(conn, org_id,person_id,org_person_rel_type, username='sysadmin'):
    cur = conn.cursor()
    sql = 'INSERT INTO ' + ORG_PERSON_TABLE + ' (org_id, person_id, org_person_rel_type,created, created_by) VALUES (?,?,?,CURRENT_TIMESTAMP,?)'
    cur.execute(sql,(org_id,person_id, org_person_rel_type,username))
    conn.commit()
    conn.close()
    return cur.lastrowid 

def add_new_person(conn, org_id, first, last, org_person_rel_type, username='sysadmin'):
    person_id = person.create_person(conn, first, last, username)
    return add_existing_person(conn, org_id, person_id, org_person_rel_type, username)
    
def remove_person(conn, org_id,person_id,reason,username):
    if not org_id and not person_id:
        return False
    try:
        cur = conn.cursor()
        sql = "SELECT EXISTS (SELECT 1 FROM " + ORG_PERSON_TABLE + " WHERE org_id = ? and person_id = ?)"
        ret = cur.execute(sql,(org_id, person_id))
        ret = ret.fetchone()[0]
        if ret==1:
            sql = "UPDATE " + ORG_PERSON_TABLE + " set active = 'no', updated_by = ?, updated = CURRENT_TIMESTAMP WHERE org_id = ? and person_id = ?"
            cur.execute(sql,(username, org_id, person_id))
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False

def read_person(conn, org_id, include_inactive = False):
    cur = conn.cursor()
    sql="SELECT OP.org_person_id, p.person_id, p.first, p.last, OPRT.org_person_rel_type," \
        " OP.created, OP.created_by, OP.updated, OP.updated_by, OP.active," \
        " (SELECT Value FROM contact_route CR " \
	    "   INNER JOIN contact_route_type CRT ON CR.contact_route_type = CRT.contact_route_type_id " \
	    "   WHERE CR.person_id = OP.person_id AND CRT.contact_route_type = 'email' LIMIT 1) As Email, " \
        " (SELECT Value FROM contact_route CR " \
	    "   INNER JOIN contact_route_type CRT ON CR.contact_route_type = CRT.contact_route_type_id " \
	    "   WHERE CR.person_id = OP.person_id AND CRT.contact_route_type = 'ground line' LIMIT 1) As Phone " \
        " FROM org_person OP " \
        " INNER JOIN org_person_rel_type OPRT ON OP.org_person_rel_type = OPRT.org_person_rel_id " \
        " INNER JOIN person p ON p.person_id = OP.person_id " \
        " WHERE OP.org_id = ? " \
        " AND OP.active " + ("IN ('yes','no')" if include_inactive == True else " = 'yes'")
    ret = cur.execute(sql,(org_id,))
    return ret.fetchall()

'''
CREATE TABLE "contact_route" (
	"contact_route_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"value"	TEXT,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"created_by"	TEXT NOT NULL,
	"updated"	TIMESTAMP,
	"updated_by"	TEXT,
	"active"	TEXT DEFAULT 'yes',
	"contact_route_type"	INTEGER NOT NULL DEFAULT 1,
	"org_id"	INTEGER,
	"person_id"	INTEGER,
	PRIMARY KEY("contact_route_id" AUTOINCREMENT),
	FOREIGN KEY("org_id") REFERENCES "org"("org_id")
)
'''
def add_contact_route(conn, org_id, name, value, contact_route_type, username = 'sysadmin'):
    cur = conn.cursor()
    sql = 'INSERT INTO ' + CONTACT_ROUTE_TABLE + ' (name, value, created, created_by, contact_route_type,org_id) VALUES (?,?,CURRENT_TIMESTAMP,?,?,?)'
    cur.execute(sql,(name,value,username,contact_route_type,org_id))
    conn.commit()
    conn.close()
    return cur.lastrowid 

def update_contact_route(conn, contact_route_id, name, value,username):
    try:
        cur = conn.cursor()
        sql = 'UPDATE ' + CONTACT_ROUTE_TABLE + ' SET name = ?, value = ?, updated = CURRENT_TIMESTAMP, updated_by = ? WHERE contact_route_id = ?'
        cur.execute(sql,(name,value,username,contact_route_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def delete_contact_route(conn, contact_route_id, username):
    try:
        cur = conn.cursor()
        sql = "UPDATE " + CONTACT_ROUTE_TABLE + " SET active='no', updated = CURRENT_TIMESTAMP, updated_by = ? WHERE contact_route_id = ?"
        cur.execute(sql,(username,contact_route_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def read_contact_route(conn, org_id,include_inactive = False):
    cur = conn.cursor()
    sql="SELECT cr.contact_route_id, cr.name, cr.value," \
        " cr.created, cr.created_by, cr.updated," \
        " cr.updated_by, crt.contact_route_type," \
        " (SELECT address_type from address_type AT" \
        " WHERE AT.address_type_id = CR.address_type_id) AS AddressType" \
        " FROM contact_route CR" \
        " INNER JOIN contact_route_type crt on crt.contact_route_type_id = cr.contact_route_type" \
        " WHERE cr.org_id = ?" \
        " AND CR.active " + ("IN ('yes','no')" if include_inactive == True else " = 'yes'")
    ret = cur.execute(sql,(org_id,))
    return ret.fetchall()    

'''
CREATE TABLE "contact_route" (
	"contact_route_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"value"	TEXT,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"created_by"	TEXT NOT NULL,
	"updated"	TIMESTAMP,
	"updated_by"	TEXT,
	"active"	TEXT DEFAULT 'yes',
	"contact_route_type"	INTEGER NOT NULL DEFAULT 1,
	"org_id"	INTEGER,
	"person_id"	INTEGER,
	"address_id"	INTEGER,
	"address_type_id"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("contact_route_id" AUTOINCREMENT),
	FOREIGN KEY("org_id") REFERENCES "org"("org_id")
)
'''
def add_address(conn, org_id,address_1, address_2, town, state, zip, country_id, address_type_id, username = 'sysadmin'):
    cur = conn.cursor()
    address_id = address.create_address(conn, address_1, address_2, town, state, zip, country_id, username)
    sql = 'INSERT INTO ' + CONTACT_ROUTE_TABLE + ' (created, created_by, contact_route_type,org_id, address_id, address_type_id) VALUES (CURRENT_TIMESTAMP,?,?,?,?,?)'
    cur.execute(sql,(username,CONTACT_ROUTE_TYPE_POSTAL_ADDRESS,org_id, address_id, address_type_id))
    conn.commit()
    conn.close()
    return cur.lastrowid

def update_address(conn, contact_route_id,address_1, address_2, town, state, zip, country_id, username = 'sysadmin'):
    try:
        cur = conn.cursor()
        print("Creating address")
        address_id = address.create_address(conn, address_1, address_2, town, state, zip, country_id, username)
        print('address_id : ' + str(address_id))
        sql = 'UPDATE ' + CONTACT_ROUTE_TABLE + ' SET address_id =?, updated = CURRENT_TIMESTAMP, updated_by = ? WHERE contact_route_id = ?'
        cur.execute(sql,(address_id, username,contact_route_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def delete_address(conn, contact_route_id, username):
    return delete_contact_route(conn,contact_route_id, username)

def read_address(conn, org_id, include_inactive = False):
    cur = conn.cursor()
    sql="SELECT CR.contact_route_id, A.address_id," \
        " A.address_line_1, A.address_line_2, A.town, A.state, A.zip, C.name," \
        " CR.created, CR.created_by, CR.updated, CR.updated_by" \
        " FROM contact_route CR" \
        " INNER JOIN Address A ON CR.address_id = A.address_id" \
        " INNER JOIN Address_Type AT ON CR.address_type_id = AT.address_type_id" \
        " INNER JOIN Country C ON A.country_id = C.country_id" \
        " WHERE CR.org_id = ?" \
        " AND CR.active " + ("IN ('yes','no')" if include_inactive == True else " = 'yes'")
    ret = cur.execute(sql,(org_id,))
    return ret.fetchall()

'''
CREATE TABLE "document" (
	"document_id"	INTEGER NOT NULL,
	"document_name"	TEXT NOT NULL,
	"document_type"	INTEGER NOT NULL DEFAULT '`',
	"document"	BLOB NOT NULL,
	"org_id"	INTEGER,
	"person_id"	INTEGER,
	"created"	INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"created_by"	TEXT NOT NULL DEFAULT 'sysadmin',
	"updated"	INTEGER,
	"updated_by"	TEXT,
	"document_format"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("person_id") REFERENCES "person"("person_id"),
	FOREIGN KEY("org_id") REFERENCES "org"("org_id"),
	PRIMARY KEY("document_id" AUTOINCREMENT)
)
'''
def add_document(conn, org_id, document_id,  username='sysadmin'):
    cur = conn.cursor()
    sql = 'UPDATE ' + DOCUMENT_TABLE + ' SET org_id = ?, updated_by = ? WHERE document_id = ?'
    cur.execute(sql,(org_id, username, document_id))
    conn.commit()
    conn.close()
    return True

def update_document(conn, document_id, document_name, document, username):
    try:
        cur = conn.cursor()
        sql = "UPDATE " + DOCUMENT_TABLE + " SET document_name = ?, document = ?, updated = CURRENT_TIMESTAMP, updated_by = ? WHERE document_id = ?"
        cur.execute(sql,(document_name, document,username, document_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def delete_document(conn, org_id, document_id, username):
    try:
        cur = conn.cursor()
        sql = "UPDATE " + DOCUMENT_TABLE + " SET active = 'no', updated = CURRENT_TIMESTAMP, updated_by = ? WHERE org_id = ? AND document_id = ?"
        cur.execute(sql,(username, org_id, document_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def read_document(conn, org_id, include_inactive = False):
    cur = conn.cursor()
    sql="SELECT d.document_id, d.document_name, d.active, d.created," \
        " d.created_by, d.updated, d.updated_by, dt.document_type, df.document_format, df.extension FROM document d" \
        " INNER JOIN document_type dt ON d.document_type = dt.document_type_id" \
        " INNER JOIN document_format df on d.document_format = df.document_format_id" \
        " WHERE d.org_id = ?" \
        " AND d.active " + ("IN ('yes','no')" if include_inactive == True else " = 'yes'")
    ret = cur.execute(sql,(org_id,))
    return ret.fetchall() 