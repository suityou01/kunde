from aiohttp import web
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

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

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

    app.router.add_static('/',path='',name='static')

    web.run_app(app, port=8085)