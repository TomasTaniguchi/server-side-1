import web

async def handle(request):
    name = request.match_info.get('id_name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{id_name}', handle)])

if __name__ == '__main__':
    web.run_app(app)