import asyncio
from aiohttp import web
from aiohttp_validate import validate
import datetime
import json
import logging
import os
import sys
sys.path.append(os.path.abspath('../model'))
import model
from model import document, org, db
from schema.org_schema import new_org_schema, update_org_schema, \
delete_org_schema, search_org_schema, new_org_person_schema, remove_org_person_schema, \
search_org_person_schema, new_org_contact_route_schema, update_org_contact_route_schema, delete_org_contact_route_schema, \
read_org_contact_route_schema, new_org_address_schema, update_org_address_schema, delete_org_address_schema, read_org_address_schema, \
new_org_doc_schema, search_org_doc_schema
import time

#*****************************************************************************************************************************************
# Api endpoints
#*****************************************************************************************************************************************

@validate(request_schema=new_org_schema)
async def add_org(request, *args):
    nm = request['name']
    a1 = request['address_1']
    a2 = request['address_2']
    tn = request['town']
    st = request['state']
    zp = request['zip']
    ct = request['country']
    un = request['username']
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    org_id = model.org.create_org(conn,nm,un)
    model.org.add_address(conn,org_id,a1,a2,tn,st,zp,ct,1,un)
    return web.json_response(org_id)
    
@validate(request_schema=update_org_schema)
async def update_org(request, *args):
    id = request['org_id']
    nm = request['name']
    un = request['username']
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.update_org(conn,id,nm,un))

@validate(request_schema=delete_org_schema)
async def delete_org(request, *args):
    id = request['org_id']
    un = request['username'] 
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.delete_org(conn,id,un))

@validate(request_schema=search_org_schema)
async def read_org(request,*args):
    id = request.get("org_id") or None
    nm = request.get("name") or "%"
    zp = request.get("zip") or "%"
    ia = request["include_inactive"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    if id:
        return web.json_response(model.org.read_org_by_id(conn,id))
    else:    
        return web.json_response(model.org.read_org(conn,zp,nm))

@validate(request_schema=new_org_person_schema)
async def add_person(request,*args):
    id = request["org_id"]
    pi = request.get("person_id") or None
    fn = request.get("first")
    ln = request.get("last")
    rt = request["rel_type"]
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    if pi:
        return web.json_response(model.org.add_existing_person(conn,id,pi,rt,un))
    else:
        return web.json_response(model.org.add_new_person(conn,id,fn,ln,rt,un))

@validate(request_schema=remove_org_person_schema)
async def remove_person(request,*args):
    id = request["org_id"]
    pi = request["person_id"]
    rn = request.get("reason")
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.remove_person(conn,id,pi,rn,un))

@validate(request_schema=search_org_person_schema)
async def read_person(request,*args):
    id = request["org_id"]
    ia = request["include_inactive"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.read_person(conn,id,ia))

@validate(request_schema=new_org_contact_route_schema)
async def add_contact_route(request,*args):
    id = request["org_id"]
    nm = request["name"]
    vl = request["value"]
    ct = request["contact_route_type"]
    un = request.get("username")
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.add_contact_route(conn,id,nm,vl,ct,un))

@validate(request_schema=update_org_contact_route_schema)
async def update_contact_route(request,*args):
    id = request["contact_route_id"]
    nm = request["name"]
    vl = request["value"]
    un = request.get("username")
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.update_contact_route(conn,id,nm,vl,un))

@validate(request_schema=delete_org_contact_route_schema)
async def delete_contact_route(request,*args):
    id = request["contact_route_id"]
    un = request.get("username")
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return (model.org.delete_contact_route(conn,id,un))

@validate(request_schema=read_org_contact_route_schema)
async def read_contact_route(request,*args):
    id = request["org_id"]
    ia = request["include_inactive"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.read_contact_route(conn,id,ia))

@validate(request_schema=new_org_address_schema)
async def add_address(request,*args):
    id = request["org_id"]
    a1 = request["address_1"]
    a2 = request.get("address_2")
    tn = request["town"]
    st = request.get("state")
    zp = request.get("zip")
    ci = request["country_id"]
    at = request["address_type_id"]
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.add_address(conn,id,a1,a2,tn,st,zp,ci,at,un))

@validate(request_schema=update_org_address_schema)
async def update_address(request,*args):
    id = request["contact_route_id"]
    a1 = request["address_1"]
    a2 = request.get("address_2")
    tn = request["town"]
    st = request.get("state")
    zp = request.get("zip")
    ci = request["country_id"]
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.update_address(conn,id,a1, a2, tn, st, zp, ci, un))

@validate(request_schema=delete_org_address_schema)
async def delete_address(request,*args):
    id = request["contact_route_id"]
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.delete_address(conn,id,un))

@validate(request_schema=read_org_address_schema)
async def read_address(request,*args):
    id = request["org_id"]
    ia = request["include_inactive"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.read_address(conn,id,ia))

async def upload_document(request):
    data = await request.post()
    document = data['file']
    username = data['username']
    document_id = data.get('document_id')
    filename, filext = os.path.splitext(document.filename)
    conn = create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    ret = model.document.upload_document(conn, document.file,filename,document.content_type,filext,username, document_id=document_id)
    return web.json_response(ret) 

@validate(request_schema=new_org_doc_schema)
async def add_document(request,*args):
    id = request["org_id"]
    di = request["document_id"]
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.add_document(conn,id,di,un))

@validate(request_schema=new_org_doc_schema)
async def delete_document(request, *args):
    id = request["org_id"]
    di = request["document_id"]
    un = request["username"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.delete_document(conn,id,di,un))

@validate(request_schema=search_org_doc_schema)
async def read_document(request, *args):
    id = request["org_id"]
    ia = request["include_inactive"]
    conn = model.db.create_connection(os.path.join(os.path.dirname(__file__), '../db/kunde.db'))
    return web.json_response(model.org.read_document(conn,id,ia))

#*****************************************************************************************************************************************
# App start up code below here only
#*****************************************************************************************************************************************

async def on_startup(userapi):
    #log.info("org sub_app startup")
    print("org sub_app startup")
    
async def on_shutdown(userapi):
    #log.info("org sub_app shutdown")
    print("org sub_app shutdown")

org_app = web.Application()
log = logging.getLogger(__name__)

org_app.on_shutdown.append(on_shutdown)
org_app.on_startup.append(on_startup)
org_app.add_routes([web.post('/', add_org, name='add_org')])
org_app.add_routes([web.put('/', update_org, name='update_org')])
org_app.add_routes([web.delete('/', delete_org, name='delete_org')])
org_app.add_routes([web.get('/', read_org, name='read_org')])
org_app.add_routes([web.post('/person', add_person, name='add_person')])
org_app.add_routes([web.get('/person', read_person, name='read_person')])
org_app.add_routes([web.delete('/person', remove_person, name='remove_person')])
org_app.add_routes([web.post('/contactroute', add_contact_route, name='add_contact_route')])
org_app.add_routes([web.put('/contactroute', update_contact_route, name='update_contact_route')])
org_app.add_routes([web.delete('/contactroute', delete_contact_route, name='delete_contact_route')])
org_app.add_routes([web.get('/contactroute', read_contact_route, name='read_contact_route')])
org_app.add_routes([web.post('/address', add_address, name='add_address')])
org_app.add_routes([web.put('/address', update_address, name='update_address')])
org_app.add_routes([web.delete('/address', delete_address, name='delete_address')])
org_app.add_routes([web.get('/address', read_address, name='read_address')])
org_app.add_routes([web.post('/document', add_document, name='add_document')])
org_app.add_routes([web.delete('/document', delete_document, name='delete_document')])
org_app.add_routes([web.get('/document', read_document, name='read_document')])
org_app.add_routes([web.post('/document/upload', upload_document, name='upload_document')])