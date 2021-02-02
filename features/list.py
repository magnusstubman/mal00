from features import addFeature
from lib import implants
from lib import globals

import tableprint
import timeago
import sys
import time

global lastImplantCount 
lastImplantCount = 0

def delLast(num):
  return
  num += 4
  ERASE_LINE = '\x1b[2K'
  CURSOR_UP_ONE = '\x1b[1A'
  CURSOR_DOWN_ONE = '\x1b[1B'
  print((CURSOR_UP_ONE + ERASE_LINE) * num, end='', flush=True)
  #print((CURSOR_UP_ONE + ERASE_LINE) * num, end='', flush=False)
  #print((CURSOR_UP_ONE ) * num, end='', flush=True)
  #print((CURSOR_DOWN_ONE ) * num, end='', flush=True)
  #sys.stdout.flush()
  time.sleep(2)

class ListCommand:
  command = 'list'

  def run(arguments, inf):
    if not arguments or (arguments and len(arguments) == 0):
      if len(implants.implants) > 0:
        global lastImplantCount
        if globals.lastCommand == ListCommand.command:
          delLast(lastImplantCount)
          
        
        #headers = ['last seen', 'name', 'external', 'internal', 'user' 'host', 'os']
        #headers = ['name', 'last seen', 'external', 'computer', 'user', 'domain', 'admin', 'ip']
        headers = ['name', 'last seen', 'external']
        data = []


        for i in implants.implants:
          #entry = [timeago.format(i.lastSeen), i.name, i.host]
          #entry = [i.name, timeago.format(i.lastSeen), i.host]
          #entry = [i.name, timeago.format(i.lastSeen), i.host, i.computerName, i.userName, str(i.domain), str(i.highIntegrity), i.ip]
          entry = [i.name, timeago.format(i.lastSeen), i.host]
          data.append(entry)

        tableprint.table(data, headers, width=16)
        print('', end='', flush=True)
        lastImplantCount = len(implants.implants)
      else:
        print(str(len(implants.implants)) + ' implants', flush=True)
    else:
      if implants.implants:
        implants.implants.clear()
        implants.currentImplant = None
        print('table cleared.')
      
  def help():
    return 'lists implants. "list clear" clear the current table'


addFeature(ListCommand)
