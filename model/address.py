ADDRESS_TABLE = 'address'
'''
CREATE TABLE "address" (
	"address_id"	INTEGER NOT NULL,
	"address_line_1"	TEXT NOT NULL,
	"address_line_2"	TEXT,
	"town"	TEXT NOT NULL,
	"state"	TEXT,
	"zip"	TEXT,
	"country_id"	INTEGER NOT NULL DEFAULT 234,
	"active"	TEXT NOT NULL DEFAULT 'yes',
	"created"	INTEGER NOT NULL,
	"created_by"	TEXT NOT NULL DEFAULT 'sysadmin',
	"udpdated"	INTEGER,
	"updated_by"	TEXT,
	FOREIGN KEY("country_id") REFERENCES "country"("country_id"),
	PRIMARY KEY("address_id" AUTOINCREMENT)
)
'''
def create_address(conn, address_1, address_2, town, state, zip, country_id, username = 'sysadmin'):
    cur = conn.cursor()
    sql = "SELECT address_id FROM " + ADDRESS_TABLE + " WHERE address_line_1 = ? AND address_line_2 = ? AND town = ? AND state = ? AND zip = ? AND country_id = ? AND active = 'yes'"
    ret = cur.execute(sql,(address_1,address_2,town,state, zip, country_id))
    rows = ret.fetchall()
    if len(rows) == 0:
        sql = 'INSERT INTO ' + ADDRESS_TABLE + ' (address_line_1, address_line_2, town, state, zip, country_id, created_by) VALUES (?,?,?,?,?,?,?)'
        cur.execute(sql,(address_1, address_2 or '', town, state, zip, country_id, username))
        conn.commit()
        ret = cur.lastrowid
        return ret
    else:
        return rows[0][0]
    