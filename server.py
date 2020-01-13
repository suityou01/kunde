from aiohttp import web
import asyncio
from api.org import org_app
from controller.org import org_controller
from controller.settings import settings_controller
from controller.user import user_controller
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
app.add_subapp('/controller/org/', org_controller)
app.add_subapp('/controller/settings/', settings_controller)
app.add_subapp('/controller/user/', user_controller)

if __name__ == "__main__":
    aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('view'),
    context_processors = [aiohttp_jinja2.request_processor])

    app.router.add_static('/',path='',name='static')

    web.run_app(app, port=8085)