import asyncio
import time
from aiohttp import web

app = web.Application()
web.run_app(app, host='127.0.0.1', port=8080)

async def index(request):
    return web.Response(text='Hello Aiohttp!')