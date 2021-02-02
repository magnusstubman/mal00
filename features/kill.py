from features import addFeature
import messages
from messages import OutgoingMessage

class KillCommand:
  command = 'kill'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      message = OutgoingMessage(KillCommand.command, None)
      implant.queueOutgoingMessage(message)

  def help():
    return 'Evaluate expressions in the implant\'s native language runtime. Usage: eval Msgbox "U HACKED!"'

  def incoming(data, implant):
    print('Received unencodable kill data from ' + implant.name + ': ' + data.hex())

  def help():
    return 'kills current implant'
    


addFeature(KillCommand)
