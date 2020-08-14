from aiohttp import web

class Handler:
    def __init__(self):
        pass
    async def websocket_handler(self,request):
      ws=web.WebSocketResponse()
      await ws.prepare(request)
      async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

        

app=web.Application()
handler= Handler()
app.add_routes([web.get('/', handler.websocket_handler)])

web.run_app(app)