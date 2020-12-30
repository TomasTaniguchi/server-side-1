import aiohttp
import asyncio
from logging import log

async def main():
    payload = {'to_number': '5493764921348', 'type': 'text', 'message': 'Bienvenidos al area #gerencia, todos sus mensajes serán redirijidos a esta area     '}
    url = 'https://api.maytapi.com/api/55efec08-be5e-4045-b538-4079c9d968de/8848/sendMessage'
    header = {'Content-Type': 'application/json', 'x-maytapi-key': '96f5cb53-c274-4588-8c30-bd6bc9b9ce71'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=header, json=payload) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

print("start")
loop = asyncio.get_event_loop()
print("second")
loop.run_until_complete(main())
print("finally")
