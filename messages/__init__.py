import struct

"""
2 bytes:        implant name
1 byte:         message name length
0-255 bytes:    messagename
2 byte:         data length 
0-255^2 bytes:  length

"""

from lib import crypto
#from messages import shelloutput
#from messages import shellcommandmessage

class IncomingMessage(object):
  name = None
  implantName = None
  data = None
  host = None

  def __init__(self, buf, host):
    buf = crypto.decrypt(buf)

    self.implantName = buf[0:2].hex()

    nameLen = int(buf[2])
    self.name = str(buf[3:3+nameLen], 'ascii')

    dataLen = int(buf[3+nameLen])
    dataLen = struct.unpack('>H', buf[3+nameLen:5+nameLen])[0]
    self.data = buf[5+nameLen:5+nameLen + dataLen]

    self.host = host

    #print(self.implantName)
    #print(str(nameLen))
    #print(self.name)
    #print(str(dataLen))
    #print(self.data)

class OutgoingMessage(object):
  name = None
  data = None

  def __init__(self, name, data):
    self.name = name
    self.data = data

  def toBuf(self):
    # note no name in outgoing bufs!
    nameLen = bytes([len(self.name)])
    name = bytes(self.name, 'ascii')

    if not self.data:
      self.data = bytes('', 'ascii')
  
    dataLen = len(self.data).to_bytes(2, 'big')

    buf = nameLen + name + dataLen
    buf = buf + self.data
    
    crypto.encrypt(buf)
    
    return buf
  
buf = b'\xde\xad\x05shell\x00\x14'
buf = b'\xde\xad\x05sleep\x00\x00'
import base64
buf = str(base64.b64encode(buf), 'ascii')

#print(buf)

#buf = str(base64.b64encode(buf), 'ascii')
#message = Message(buf)

