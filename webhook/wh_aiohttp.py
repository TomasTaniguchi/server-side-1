from aiohttp import web
import multiprocessing
from rx import Observable
from rx.concurrency import ThreadPoolScheduler
from webhook import wh_procces
optimal_thread_count = multiprocessing.cpu_count() + 1
poo_scheduler = ThreadPoolScheduler(optimal_thread_count)


async def webhook(request):
    payload = await request.json()

    Observable.of(payload).map(lambda i: (i['type'])).take_while(lambda i: i == "ack") \
        .map(lambda i: wh_procces.act(payload)).subscribe_on(poo_scheduler).subscribe()

    Observable.of(payload).map(lambda i: (i['type'])).take_while(lambda i: i == "message") \
        .map(lambda i: messenger(payload)).subscribe_on(poo_scheduler).subscribe()

    return web.Response()


def messenger(payload):
    source = Observable.of(payload).map(lambda i: (i['message']['fromMe'] == True))

    source.take_while(lambda i: i == True) \
        .map(lambda i: wh_procces.message_sent(payload)).subscribe_on(poo_scheduler).subscribe()

    source.take_while(lambda i: i == False) \
        .map(lambda i: wh_procces.message_received(payload)).subscribe_on(poo_scheduler).subscribe()


app = web.Application()
app.add_routes([web.post('/webhook', webhook)])

web.run_app(app, port=8000)
