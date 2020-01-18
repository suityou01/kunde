from aiohttp import web
import aioredis
import asyncio
from api.org import org_app
from api.document import doc_app
from controller.org import org_controller
from controller.settings import settings_controller
from controller.user import user_controller
from controller.person import person_controller
from controller.lead import lead_controller
from controller.campaign import campaign_controller
from controller.opportunity import opportunity_controller
from controller.alerts import alert_controller
from controller.calendar import calendar_controller
from controller.mail import mail_controller
from controller.task import task_controller
import aiohttp_jinja2
import jinja2
import json
from pprint import pprint
import time
import threading
import uuid

async def database_event(event_type, payload):
    print("DATABASE EVENT RECEIVED")
    print("EVENT_TYPE %d" % event_type)
    pprint(payload)

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

def message_queue_worker():
    while not msg_queue_worker_stop_event.is_set():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for m in message_queue:
            try:
                msg = json.loads(message_queue[m])
                pprint(msg)
                loop.run_until_complete(asyncio.ensure_future(message_dispatch[msg['message']](msg['event_type'],msg['payload'])))
            except Exception as e:
                print(str(e))
        message_queue.clear()
        time.sleep(2)
    loop.close()
    return

async def message_listener(ch):
    try:
        while (await ch.wait_message()):
            pprint(ch)
            msg = await ch.get_json()
            pprint(msg)
            message_queue[uuid.uuid4()] = msg
    except Exception as e:
        print(str(e))

#*****************************************************************************************************************************************
# App start up code below here only
#*****************************************************************************************************************************************

async def on_startup(serverapi):
    #log.info("org sub_app startup")
    print("server startup")
    serverapi['redis'] = await aioredis.create_redis('redis://localhost')
    pub = await aioredis.create_redis('redis://localhost')
    serverapi['pub'] = pub
    sub = await aioredis.create_redis('redis://localhost')
    serverapi['sub'] = sub
    res = await sub.subscribe('system:1')
    ch1 = res[0]
    tsk = tsk = asyncio.ensure_future(message_listener(ch1))
    serverapi['tsk'] = tsk
    
async def on_shutdown(serverapi):
    #log.info("org sub_app shutdown")
    print("server shutdown")
    try:
        msg_queue_worker_stop_event.set()
        serverapi['tsk'].cancel()
        serverapi['sub'].close()
        serverapi['pub'].close()
        msg_queue_worker_thread.join()
    except Exception as e:
        #aiohttp_server_logger.info(str(e))
        print(str(e))

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])
app.add_subapp('/api/org/', org_app)
app.add_subapp('/api/document/', doc_app)
app.add_subapp('/controller/org/', org_controller)
app.add_subapp('/controller/settings/', settings_controller)
app.add_subapp('/controller/user/', user_controller)
app.add_subapp('/controller/person/', person_controller)
app.add_subapp('/controller/lead/', lead_controller)
app.add_subapp('/controller/campaign/', campaign_controller)
app.add_subapp('/controller/opportunity/', opportunity_controller)
app.add_subapp('/controller/alert/', alert_controller)
app.add_subapp('/controller/calendar/', calendar_controller)
app.add_subapp('/controller/mail/', mail_controller)
app.add_subapp('/controller/task/', task_controller)

if __name__ == "__main__":

    aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('view'),
    context_processors = [aiohttp_jinja2.request_processor])

    message_queue={}
    msg_queue_worker_stop_event = threading.Event()
    msg_queue_worker_thread = threading.Thread(target=message_queue_worker, args=())
    msg_queue_worker_thread.start()
    message_dispatch={}
    message_dispatch['database_event'] = database_event

    app.router.add_static('/',path='',name='static')
    app.on_shutdown.append(on_shutdown)
    app.on_startup.append(on_startup)

    web.run_app(app, port=8085)