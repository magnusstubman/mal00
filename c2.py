#!/usr/bin/env python3.8
print("""
     _              _ ___ ___ 
    / |   _____ ___| |   |   |
 _ / /   |     | .'| | | | | |
|_|_/    |_|_|_|__,|_|___|___|

""")

import asyncio

from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession
#from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from aiohttp import web

#######################

from lib import web
from lib import implants
from lib import globals
globals.init()

import features
import messages

async def interactive_shell():
  global autosuggest 
  autosuggest = AutoSuggestFromHistory()
  session = PromptSession(history=FileHistory('commandhistory.txt'))

  while True:
    try:
      if implants.currentImplant:
        result = await session.prompt_async('\n' + implants.currentImplant.name + ' > ', auto_suggest=AutoSuggestFromHistory())
      else:
        result = await session.prompt_async('\n> ', auto_suggest=AutoSuggestFromHistory())

      #result = await session.prompt_async()
      if len(result) > 0:
        features.parseCommand(result)
    except (EOFError, KeyboardInterrupt):
      return


def callback(buf, host):
  try:
    message = messages.IncomingMessage(buf, host)
  except Exception:
    print('could not parse message')
    return None
    

  implant = implants.getImplantByName(message.implantName)
  if not implant:
    implant = implants.addNewImplant(message.implantName, message.host)
  implant.seen(host)

  feature = features.getFeatureByName(message.name) 
  if feature:
    feature.incoming(message.data, implant)
  else:
    print('unknown command from ' + implant.name + ': ' + message.name + " " + message.data.hex())
  
  if not implant.outgoingQueueEmpty():
    #print("sending something from queue in reply...")
    return implant.dequeueOutgoingMessage().toBuf()
  
  #print("nothing in queue...")
  return None 

async def main():
  with patch_stdout():
    webTask = asyncio.create_task(web.startWebServer(callback))

    try:
      await interactive_shell()
    finally:
      pass
      webTask.cancel()
    print("Quitting event loop. Bye.")

if __name__ == "__main__":
  try:
    from asyncio import run
  except ImportError:
    asyncio.run_until_complete(main())
  else:
    asyncio.run(main())
