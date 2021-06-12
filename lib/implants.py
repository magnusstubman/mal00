import datetime

def init():
  global implants
  implants = []
  global currentImplant
  currentImplant = None

init()

def addNewImplant(name, host):
  implant = Implant(name, host)
  global implants
  implants.append(implant)
  print('[+] Implant \'' + implant.name + '\' checked in from ' + implant.host)
  return implant

def getImplantByName(name):
  global implants
  for i in implants:
    if i.name == name:
      return i
  return None

class Implant(object):
  name = None
  lastSeen = None
  outgoingMessageQueue = []
  host = None

  # following attributes are retrieved from 'info' packet from implant
  computerName = ''
  userName = ''
  highIntegrity = ''
  domain = '' 
  ip = '' 

  
  def __init__(self, name, host):
    self.name = name
    self.seen(host)

  def seen(self, host):
    self.lastSeen = datetime.datetime.now()
    self.host = host

  def outgoingQueueEmpty(self):
    return len(self.outgoingMessageQueue) == 0

  def queueOutgoingMessage(self, message):
    self.outgoingMessageQueue.append(message)

  def dequeueOutgoingMessage(self):
    return self.outgoingMessageQueue.pop(0)

if False:
  for i in range(0,3):
    impla = Implant('implant' + str(i))
    impla.lastSeen = datetime.datetime.now() - datetime.timedelta(seconds = i * 20)
    global implants
    implants.append(impla)
