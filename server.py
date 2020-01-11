from aiohttp import web
from api.org import org_app

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])
app.add_subapp('/api/org/', org_app)

if __name__ == "__main__":
    web.run_app(app, port=8085)