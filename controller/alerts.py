import asyncio
import aiohttp_jinja2
import jinja2
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
# End points
#*****************************************************************************************************************************************

@aiohttp_jinja2.template('alert_dashboard.jinja2')
async def alert_dashboard(request):
    return

#*****************************************************************************************************************************************
# App start up code below here only
#*****************************************************************************************************************************************

async def on_startup(userapi):
    #log.info("org sub_app startup")
    print("alert_controller sub_app startup")
    
async def on_shutdown(userapi):
    #log.info("org sub_app shutdown")
    print("alert_controller sub_app shutdown")

alert_controller = web.Application()
log = logging.getLogger(__name__)

alert_controller.on_shutdown.append(on_shutdown)
alert_controller.on_startup.append(on_startup)
alert_controller.add_routes([web.get('/', alert_dashboard, name='alert_dashboard')])
