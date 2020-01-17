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

async def get_document_record(request):
    return web.json_response("Test")

async def get_document(request):
    w = web.Response()
    
    in_file = open(os.getcwd() + "/api/test1.pdf", "rb")
    data = in_file.read()
    w.body = data
    w.content_type = 'application/pdf'
    return w

#*****************************************************************************************************************************************
# App start up code below here only
#*****************************************************************************************************************************************

async def on_startup(userapi):
    #log.info("org sub_app startup")
    print("doc sub_app startup")
    
async def on_shutdown(userapi):
    #log.info("org sub_app shutdown")
    print("doc sub_app shutdown")

doc_app = web.Application()
log = logging.getLogger(__name__)

doc_app.on_shutdown.append(on_shutdown)
doc_app.on_startup.append(on_startup)
doc_app.add_routes([web.get('/{id}', get_document_record, name='get_document_record')])
doc_app.add_routes([web.get('/{id}/view', get_document, name='get_document')])
